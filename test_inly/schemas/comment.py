from pydantic import BaseModel
from datetime import datetime


class CommentIn(BaseModel):
    text: str
    user_id: int
    advert_id: int


class CommentOut(BaseModel):
    text: str
    user_id: int
    advert_id: int
