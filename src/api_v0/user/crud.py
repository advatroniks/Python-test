from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from .schemas import CreateUser


async def create_user(
        session: AsyncSession,
        new_user: CreateUser
) -> User:
    user = User(**new_user.model_dump())
    session.add(user)
    await session.commit()

    return user


