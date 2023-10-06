from sqlalchemy.orm import Mapped, mapped_column

from .db_model_base import Base


class City(Base):
    """
    Model city
    """

    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )

    weather: Mapped[str]

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}"

    def __repr__(self):
        return str(self)