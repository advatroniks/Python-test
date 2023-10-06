import uuid

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .db_model_base import Base


class Picnic(Base):
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id")
    )
    time: Mapped[datetime]

    def __str__(self):
        return f"{self.__class__.__name__}  id - {self.id}"
