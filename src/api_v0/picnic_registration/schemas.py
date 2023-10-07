import uuid

from pydantic import BaseModel


class RegistrationUserPicnic(BaseModel):
    user_id: uuid.UUID
    picnic_id: uuid.UUID


class RegistrationUserResponse(BaseModel):
    id: uuid.UUID