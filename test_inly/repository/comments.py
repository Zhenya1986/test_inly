import datetime

from models.models import Comment
from sqlalchemy import insert, delete, select
from repository.user import UserRepository
from schemas.comment import CommentIn, CommentOut
from db_helper import get_db


class CommentNotFound(Exception): ...


class CommentRepository:
    def __init__(self):
        self._db = get_db()
        self._table = Comment
        self._user_repository = UserRepository()

    async def create_comment(self, data: CommentIn) -> CommentOut | None:
        user = await self._user_repository.get_user(data.user_id)
        if not user:
            return None

        stmt = (
            insert(self._table)
            .values(**data.model_dump(), created_at=datetime.datetime.now())
            .returning(self._table)
        )
        result = await self._db.fetch_one(stmt)
        return CommentOut(**result)

    async def del_comment(self, comment_id: int):
        stmt = delete(self._table).where(self._table.id == comment_id)
        await self._db.execute(stmt)

    async def get(self, comment_id: int) -> CommentOut | None:
        result = await self._db.fetch_one(
            select(self._table).where(self._table.id == comment_id)
        )
        return CommentOut(**result) if result else None
