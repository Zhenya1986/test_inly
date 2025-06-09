from datetime import datetime
from db_helper import get_db
from models.models import AdvertType, Advert
from schemas.advert import AdvertOut
from models.models import User, Comment
from sqlalchemy import select, insert, delete


class UserNotFound(Exception): ...


class AdvertNotFound(Exception): ...


class CurrentUserError(Exception): ...


class AdvertRepository:
    def __init__(self):
        self._db = get_db()
        self._table = Advert
        self._user = User
        self._comment = Comment

    async def create_advert(
        self,
        title: str,
        description: str,
        advert_type: AdvertType,
        user_id: int,
        is_active: bool,
    ):

        user = await self._db.fetch_one(
            select(self._user).where(self._user.id == user_id)
        )

        if not user:
            raise UserNotFound(f"Нет пользователя с таким ID({user_id})!")

        stmt = (
            insert(self._table)
            .values(
                title=title,
                description=description,
                type=advert_type,
                user_id=user_id,
                is_active=is_active,
                created_at=datetime.now(),
            )
            .returning(self._table)
        )

        result = await self._db.fetch_one(stmt)
        return AdvertOut(**result)

    async def delete_advert(self, advert_id: int):
        await self._db.execute(delete(self._table).where(self._table.id == advert_id))

    async def get_list_advert(
        self,
        offset: int,
        limit: int,
        advert_type: AdvertType | None,
        is_active: bool,
    ) -> list[AdvertOut]:
        query = (
            select(self._table)
            .join(self._comment, self._comment.advert_id == self._table.id)
            .where(self._table.is_active == is_active)
        )

        if advert_type is not None:
            query = query.where(self._table.type == advert_type)

        query = (
            query.order_by(self._table.created_at.desc()).offset(offset).limit(limit)
        )
        query.compile(compile_kwargs={"literal_binds": True})
        result = await self._db.fetch_all(query)

        return [AdvertOut(**row) for row in result]


    async def get(self, advert_id: int) -> AdvertOut | None:
        result = await self._db.fetch_one(
            select(self._table).where(self._table.id == advert_id)
        )
        return AdvertOut(**result) if result else None


    async def get_full(self, advert_id: int):
        result = await self._db.fetch_all(
            select(self._table, self._comment)
            .join(self._comment, self._comment.advert_id == self._table.id)
            .where(self._table.id == advert_id)
        )
        return result
