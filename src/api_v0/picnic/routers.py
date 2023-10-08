import uuid
from datetime import datetime

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Query, HTTPException, status


from src.models import db_helper
from .schemas import CreatePicnic, ResponseAllPicnics, CreatedPicnicResponse
from . import crud

router = APIRouter(
    tags=["picnics"]
)


@router.post(
    path="/create_picnic",
    response_model=CreatedPicnicResponse
)
async def create_picnic(
        picnic: CreatePicnic,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер для создания пикника. Так же здесь осуществляется проверка времени.
    Время создаваемого пикника не должно быть меньше текущего.
    :param picnic: CreatePicnic(Pd obj) параметры для нового пикника.
    :param session: AsyncSession obj
    :returns: CreatePicnicResponse (Pd obj)
    :raises HTTPException: Если время создания пикника < чем текущее на сервере. 400 BAD REQUEST.
    """
    if picnic.time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't add picnic in past, check picnic data!"
        )

    return await crud.create_picnic(
        picnic=picnic,
        session=session
    )


@router.get(
    path="/all_picnics",
    response_model=list[ResponseAllPicnics]
)
async def get_all_picnics_with_users(
        date_time: Annotated[
            datetime,
            Query(
                description="Picnic time, on default not defined"
            )
        ] = None,
        past: Annotated[
            bool,
            Query(
                description="Include passed picnics"
            )
        ] = True,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер возвращает все пикники и юзеров, которые были зарегистрированы на конкретный пикник.
    :param date_time: Datetime ЕСЛИ УКАЗАНО, ТО ВРЕМЯ В КОТОРОЕ проводятся пикники.
    :param past: Указатель, если True, то в ответ включаются прошедшие пикники. Если False только грядущие.
    :param session: AsyncSession obj
    :returns: List[ResponseAllPicnics] лист всех (Pd objects) пикников, в зависимости от параметров.
    """
    return await crud.get_picnics_with_users(
        session=session,
        past=past,
        picnic_date=date_time
    )


@router.get(
    path="/picnic{picnic_id}",
    response_model=ResponseAllPicnics
)
async def get_picnic_with_users_by_id(
        picnic_id: uuid.UUID,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер возвращает пикник с конкретным id(UUID)
    :param picnic_id: UUID пикника.
    :param session: AsyncSession obj
    :returns: ResponseAllPicnics (Pd object) Пикник по заданному ID(UUID) со всеми игроками.
    """
    lists_response = await crud.get_picnics_with_users(
            session=session,
            picnic_id=picnic_id
    )

    return lists_response[0]
