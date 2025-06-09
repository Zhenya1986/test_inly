from db_helper import get_db
from models.models import User
from schemas.user import UserOut, UserIn, UserUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, delete, update
from auth.utils import verify_password


class DoubleNameException(Exception): ...


class UserNotFound(Exception): ...


class UserRepository:
    def __init__(self):
        self._db = get_db()
        self._table = User

    async def create_user(
        self,
        data: UserIn,
        hash_password: bytes,
        is_admin: bool,
        is_banned: bool,
    ) -> UserOut:
        stmt = (
            insert(self._table)
            .values(
                username=data.username,
                password=hash_password,
                is_admin=is_admin,
                is_banned=is_banned,
            )
            .returning(self._table)
        )
        try:
            result = await self._db.fetch_one(stmt)
        except IntegrityError:
            raise DoubleNameException("User already exist")
        return UserOut(**result)

    async def del_user(self, user_id: int):
        stmt = delete(self._table).where(self._table.id == user_id)
        await self._db.execute(stmt)

    async def get_user(self, user_id: int | None = None, token: str | None = None) -> UserOut | None:
        stmt = select(self._table)
        if user_id:
            stmt = stmt.where(self._table.id == user_id)
        if token:
            stmt = stmt.where(self._table.token == token)

        user = await self._db.fetch_one(stmt)
        return UserOut(**user) if user else None

    async def authenticate_user(self, username: str, password: str) -> UserOut | None:
        result = await self._db.fetch_one(
            select(self._table).where(self._table.username == username)
        )
        if not result:
            return None

        if not verify_password(password, result.password):
            return None

        return UserOut(**result)

    async def update(
        self,
        user_id: int,
        user_update: UserUpdate,
    ) -> UserOut:
        result = await self._db.fetch_one(
            update(self._table)
            .where(self._table.id == user_id)
            .values(**user_update.model_dump(exclude_unset=True))
            .returning(self._table)
        )
        return UserOut(**result)



