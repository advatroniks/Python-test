from datetime import datetime

from pydantic import BaseModel


class CreatePicnic(BaseModel):
    city_name: str
    time: datetime



