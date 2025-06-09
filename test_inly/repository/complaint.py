import datetime
from models.models import Complaint
from sqlalchemy import insert, delete, select
from repository.user import UserRepository
from db_helper import get_db
from schemas.complaint import ComplaintOut, ComplaintIn


class ComplaintRepository:
    def __init__(self):
        self._db = get_db()
        self._table = Complaint
        self._user_repository = UserRepository()

    async def create_complaint(self, data: ComplaintIn) -> ComplaintOut | None:
        user = await self._user_repository.get_user(data.user_id)
        if not user:
            return None

        stmt = (
            insert(self._table)
            .values(**data.model_dump(), created_at=datetime.datetime.now())
            .returning(self._table)
        )
        result = await self._db.fetch_one(stmt)
        return ComplaintOut(**result)

    async def del_complaint(self, complaint_id: int):
        stmt = delete(self._table).where(self._table.id == complaint_id)
        await self._db.execute(stmt)

    async def get(self, complaint_id: int) -> ComplaintOut | None:
        result = await self._db.fetch_one(
            select(self._table).where(self._table.id == complaint_id)
        )
        return ComplaintOut(**result) if result else None


    async def get_list_complaint(self, advert_id: int, limit: int, is_approved: bool) -> list[ComplaintOut]:
        query = (
            select(self._table)
            .where(
                self._table.advert_id == advert_id,
                self._table.is_approved == is_approved,
            )
            .order_by(self._table.created_at.desc())
            .limit(limit)
        )
        result = await self._db.fetch_all(query)
        return [ComplaintOut(**row) for row in result]
