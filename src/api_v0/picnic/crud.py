import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.api_v0.user.schemas import ResponseUser
from src.models import Picnic, PicnicRegistration
from src.api_v0.city.crud import get_all_cities_or_scalar_city
from .schemas import CreatePicnic, ResponseAllPicnics


async def create_picnic(
        picnic: CreatePicnic,
        session: AsyncSession,
) -> Picnic:
    """
    Функция создает пикник в базе данных. Принимает(CreatePicnic (Pd obj))
    Возвращает созданный new_picnic(Picnic obj)
    :param picnic: CreatePicnic(Pd obj), модель Pydantic.
    :param session: AsyncSession obj
    :returns: new_picnic (Picnic obj) созданный и записанный в бд Picnic(sqlalchemy obj)
    """
    city = await get_all_cities_or_scalar_city(   # Получение города по названию(проверка есть ли такой город в БД).
        city=picnic.city_name,
        session=session
    )
    new_picnic = Picnic(
        city_id=city.id,
        time=picnic.time,
    )
    session.add(new_picnic)
    await session.commit()

    return new_picnic


async def get_picnic_by_id(
        session: AsyncSession,
        picnic_id: uuid.UUID
) -> Picnic:
    """
    Получение объекта Picnic(sqlalchemy obj) !!!БЕЗ USERS!!!. Функция для проверки
    существование Picnic по id не нагружая БД.
    :param session: AsyncSession obj
    :param picnic_id: UUID
    :returns: picnic Picnic(sqlalchemy obj).
    :raises HTTPException: NOT FOUND 404, если пикник не найден в БД.
    """
    stmt = select(Picnic).where(Picnic.id == picnic_id)
    result = await session.execute(statement=stmt)
    picnic = result.scalar_one_or_none()

    if picnic is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picnic can not found, check picnic id"
        )

    return picnic


async def get_picnics_with_users(
        session: AsyncSession,
        picnic_id: uuid.UUID | None = None,
        picnic_date: datetime | None = None,
        past: bool = True

) -> list[ResponseAllPicnics]:
    """
    Функция для получения списка всех пикников/пикника вместе с объектами Users, которые
    были зарегистрированы на момент выполнения функции.
    :param session: AsyncSession obj
    :param picnic_id: UUID, если None, то запрос идет ко всем объектам Picnic
    :param picnic_date: datetime, ДАТА C ТОЧНОСТЬЮ ДО МИНУТ. Параметр для получения пикника в этот момент.
    :param past: Если True, то турниры ВКЛЮЧАЯ ПРОШЕДШТЕ, если False, то только грядущие.
    :returns: List[ResponseAllPicnics]. Список всех пикников(включая зарегистрированных участников.
    :raises HTTPException: Если не найдено ни одного пикника NOT FOUND 404
    """
    stmt = (
        select(Picnic)
        .options(
            selectinload(Picnic.picnics_reg)   # Так как связь ко многим, то релевантнее Selectinload
            .joinedload(PicnicRegistration.user),      # чем Joinedload.
            joinedload(Picnic.city)
        )
    )

    if picnic_date is not None:
        stmt = stmt.where(Picnic.time == picnic_date)

    if not past:
        stmt = stmt.where(Picnic.time >= datetime.now())

    if picnic_id:
        stmt = stmt.where(Picnic.id == picnic_id)

    picnics_seq_or_instance = await session.scalars(statement=stmt)

    picnics_all = picnics_seq_or_instance.all()    # Проверка на то, что есть хотя бы ОДИН пикник.
    if not picnics_all:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found any picnics, check id key or statement! "
        )

    total_response = []
    for picnic in picnics_all:
        result = ResponseAllPicnics.model_validate(picnic, from_attributes=True)   # Sqlalchemy >> Pydantic model ser.

        for user in picnic.picnics_reg:
            result.users.append(
                ResponseUser.model_validate(user.user, from_attributes=True)   # Sqlalchemy >> Pydantic model ser.
            )

        total_response.append(result)

    return total_response
