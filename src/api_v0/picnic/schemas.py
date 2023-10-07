import uuid
from datetime import datetime

from pydantic import BaseModel

from src.api_v0.user.schemas import ResponseUser


class CreatePicnic(BaseModel):
    city_name: str
    time: datetime


class ResponseAllTournaments(BaseModel):
    picnic_id: uuid.UUID
    city: str
    city_temperature: str
    time: datetime
    users: list[ResponseUser] = []

    class Config:
        orm_mode=True


