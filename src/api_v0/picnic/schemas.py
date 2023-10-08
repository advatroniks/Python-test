import uuid
from datetime import datetime

from pydantic import BaseModel


from src.api_v0.user.schemas import ResponseUser
from src.api_v0.city.schemas import ResponseCity


class CreatePicnic(BaseModel):    # Схема для описания входящих полей для создания пикника.
    city_name: str
    time: datetime


class CreatedPicnicResponse(CreatePicnic):  # Схема для ответа на создание объекта пикника в БД.
    id: uuid.UUID


class ResponseAllPicnics(BaseModel):   # Схема для получения ответа для пикника с пользователями и городом.
    id: uuid.UUID
    city: ResponseCity
    time: datetime
    users: list[ResponseUser] = []



