import uuid
from datetime import datetime

from pydantic import BaseModel


from src.api_v0.user.schemas import ResponseUser
from src.api_v0.city.schemas import ResponseCity


class CreatePicnic(BaseModel):
    city_name: str
    time: datetime


class ResponseAllTournaments(BaseModel):
    id: uuid.UUID
    city: ResponseCity
    time: datetime
    users: list[ResponseUser] = []



