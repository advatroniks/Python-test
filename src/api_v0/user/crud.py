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
    """
    Функция для создания юзера в БД.
    :param session: AsyncSession obj
    :param new_user: CreateUser (Pd obj)
    :returns: User (Sqlalchemy obj
    """
    user = User(**new_user.model_dump())
    session.add(user)
    await session.commit()

    return user


async def get_all_users_or_scalar_user(
        session: AsyncSession,
        min_age: int | None = None,
        max_age: int | None = None,
        user_id: uuid.UUID | None = None,
) -> list[User] | User:
    """
    Функция для получения юзера по id(uuid), если не указано, то всех.
    :param session: AsyncSession obj
    :param min_age: Минимальный возраст для выборки. Если не указано, то нет нижней границы.
    :param max_age: Максимальный возраст для выборки. Если не указано, то нет верхней границы.
    :param user_id: Если указано, то юзер с конкретным id(UUID), если нет, то все юзера по выборке.
    :returns: List[User] | User список User(Sqlalchemy obj) или Один User(Sqlalchemy obj).
    :raises HTTPException: NOT FOUND 404 если User не найден или не найдено ни одного User obj в БД.
    """
    stmt = select(User)
    if user_id:
        stmt = stmt.where(User.id == user_id)

    if min_age:
        stmt = stmt.where(User.age >= min_age)

    if max_age:
        stmt = stmt.where(User.age <= max_age)

    users = await session.execute(statement=stmt)
    users_seq = users.scalars().all()

    if not users_seq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User(s) not found in database, try again please!"
        )
    if len(users_seq) == 1:
        return users_seq[0]
    return [city for city in users_seq]
