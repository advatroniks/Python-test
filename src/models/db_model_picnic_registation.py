import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .db_model_base import Base
from .db_model_user import User
from .db_model_picnic import Picnic


class PicnicRegistration(Base):
    """
    Picnic registration model
    """

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id')
    )

    picnic_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('picnics.id')
    )

    user: Mapped[User] = relationship(back_populates="picnics_reg")

    picnic: Mapped["Picnic"] = relationship(back_populates="picnics_reg")

    def __str__(self):
        return f'{self.__class__.__name__} - id {self.id}'

