import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from src.api_v0.user.crud import get_all_users_or_scalar_user
from src.api_v0.picnic.crud import get_picnic_by_id

from .service import check_actual_date
from .schemas import RegistrationUserPicnic, RegistrationUserResponse
from . import crud


router = APIRouter(
    tags=["registration_picnic"]
)


@router.post(
    path="/registration_for_picnic",
    response_model=RegistrationUserResponse
)
async def registration_for_picnic(
        picnic_registration: RegistrationUserPicnic,
        session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    """
    Роутер для создания сущности регистрация на пикник.(Many2Many).
    Функция принимает объект pydantic для создания сущности. Далее проверяется,
    существует ли пикник по-заданному ID, проверяется, актуальное ли время
    (нельзя создать сущность в прошлом). После проверяется, есть ли юзер с
    указанным user_id в picnic_registration(Pd obj). После возвращается
    (Pd obj) RegistrationUserPicnic.
    :param picnic_registration: Pydantic object
    :param session: AsyncSession obj.
    :returns: RegistrationUserResponse, при успешной регистрации юзера.
    """
    picnic = await get_picnic_by_id(
        session=session,
        picnic_id=picnic_registration.picnic_id

    )

    check_actual_date(picnic.time)

    await get_all_users_or_scalar_user(
        session=session,
        user_id=picnic_registration.user_id
    )

    return await crud.add_user_for_registration_picnic(
        new_registration=picnic_registration,
        session=session
    )




