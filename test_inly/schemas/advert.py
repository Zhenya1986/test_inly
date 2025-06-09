from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum


class AdvertType(StrEnum):
    VEHICLE = "vehicle"
    ELECTRONICS = "electronics"


class AdvertIn(BaseModel):
    advert_id: int
    title: str
    description: str
    type: AdvertType
    user_id: int
    is_active: bool = True


class AdvertOut(BaseModel):
    id: int
    title: str
    description: str
    type: AdvertType
    user_id: int
    created_at: datetime
