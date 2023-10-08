from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from .schemas import CreateUser, ResponseUser
from .dependences import validate_age_parameter, validate_age_for_add
from . import crud

router = APIRouter(tags=["users"])


@router.post(
    path="/create",
    response_model=ResponseUser
)
async def register_user(
        new_user: CreateUser,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер для создания юзера. Проверяет на 0 < age < 100 возраст так же.
    Возвращает юзера, записанного в БД.
    :param new_user: CreateUser(Pd obj)
    :param session: AsyncSession obj
    :returns: ResponseUser (Pd obj)
    """
    validate_age_for_add(new_user.age)

    return await crud.create_user(
            session=session,
            new_user=new_user
    )


@router.get(
    path="/get_all",
    response_model=list[ResponseUser]
)
async def get_all_users(
        age_parameters: dict[str, int] = Depends(validate_age_parameter),
        session: AsyncSession = Depends(db_helper.get_session_dependency)

):
    """
    Функция получения всех юзеров, если не указаны параметры
    минимальный и максимальный возраст, то все юзера.
    :param age_parameters: dict(min: value, max:value)
    :param session: AsyncSession obj
    :returns: List[ResponseUser] (Pd obj)
    """
    return await crud.get_all_users_or_scalar_user(
        session=session,
        min_age=age_parameters["min_age"],
        max_age=age_parameters["max_age"]
    )
