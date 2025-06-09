from pydantic import BaseModel
from datetime import datetime


class ComplaintIn(BaseModel):
    text: str
    user_id: int
    advert_id: int
    is_approved: bool

class ComplaintOut(BaseModel):
    text: str
    user_id: int
    advert_id: int
    is_approved: bool