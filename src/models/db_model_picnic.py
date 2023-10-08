import uuid

from typing import Set, TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db_model_base import Base

if TYPE_CHECKING:
    from .db_model_city import City
    from .db_model_picnic_registation import PicnicRegistration
    from .db_model_user import User


class Picnic(Base):
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id")
    )
    time: Mapped[datetime]

    city: Mapped["City"] = relationship(back_populates="picnics")

    picnics_reg: Mapped[list["PicnicRegistration"]] = relationship(back_populates="picnic")

    def __str__(self):
        return f"{self.__class__.__name__}  id - {self.id}"
