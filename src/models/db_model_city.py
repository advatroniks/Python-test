from sqlalchemy.orm import Mapped, mapped_column

from .db_model_base import Base


class City(Base):
    """
    Model city
    """

    name: Mapped[str]