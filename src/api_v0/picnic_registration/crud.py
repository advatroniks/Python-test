from sqlalchemy.ext.asyncio import AsyncSession

from src.models import PicnicRegistration
from .schemas import RegistrationUserPicnic


async def add_user_for_registration_picnic(
        new_registration: RegistrationUserPicnic,
        session: AsyncSession

):
    new_registration = PicnicRegistration(**new_registration.model_dump())

    session.add(new_registration)
    await session.commit()

    return new_registration
