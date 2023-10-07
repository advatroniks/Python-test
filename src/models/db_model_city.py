from typing import  TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db_model_base import Base


if TYPE_CHECKING:
    from .db_model_picnic import Picnic


class City(Base):
    """
    Model city
    """
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )

    weather: Mapped[str]

    picnics: Mapped[list["Picnic"]] = relationship(back_populates="city")

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}"

    def __repr__(self):
        return str(self)