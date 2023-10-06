from sqlalchemy.orm import Mapped

from .db_model_base import Base


class User(Base):
    """
    user
    """

    name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int]

    def __str__(self):
        return f"{self.__class__.__name__} {self.name} {self.surname}"

    def __repr__(self):
        return str(self)