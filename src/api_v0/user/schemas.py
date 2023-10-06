import uuid

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    name: str
    surname: str
    age: int


class ResponseUser(CreateUser):
    id: uuid.UUID

