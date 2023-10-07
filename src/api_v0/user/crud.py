import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException, status

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


async def get_user_by_id(
        session: AsyncSession,
        user_id: uuid.UUID,
) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(statement=stmt)
    user = result.scalar_one_or_none()

    if user is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found, try again please!"
        )
    return user


