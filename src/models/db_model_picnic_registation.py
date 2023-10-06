import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .db_model_base import Base


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

    user = relationship('User', backref='users')
    picnic = relationship('Picnic', backref='picnics')

    def __str__(self):
        return f'{self.__class__.__name__} - id {self.id}'

