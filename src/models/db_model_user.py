from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from .db_model_base import Base

if TYPE_CHECKING:
    from .db_model_picnic_registation import PicnicRegistration
    from .db_model_picnic import Picnic

class User(Base):
    """
    user
    """

    name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int]

    picnics_reg: Mapped["PicnicRegistration"] = relationship(
        back_populates="user"
    )

    def __str__(self):
        return f"{self.__class__.__name__} {self.name} {self.surname}"

    def __repr__(self):
        return str(self)