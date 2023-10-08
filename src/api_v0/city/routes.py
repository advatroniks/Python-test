from typing import Annotated

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from .schemas import CreateCity, ResponseCity
from . import crud

router = APIRouter(tags=["/cities"])


@router.post(
    path="/create_city",
    response_model=ResponseCity
)
async def create_city(
        city: CreateCity,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер принимает CreateCity(Pd object). Возвращает
    ResponseCity(Pd object) результат работы create_city.
    :param city: CreateCity(Pd object)
    :param session: AsyncSession object
    :returns: ResponseCity(Pd object) - созданный город
    """
    return await crud.create_city(
            new_city=city,
            session=session
    )


@router.get(
    path="/get_cities",
    response_model=list[ResponseCity] | ResponseCity
)
async def get_city_by_name(
        city_name: Annotated[str, Query(
            max_length=20,
            description="City name for request"
        )
        ] = None,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер принимает city_name(str), где проверяется на длину(< 20 char),
    не обязательный параметр. Если city_name не задан, то возвращает list[ResponseCity(PD obj),
    если имя города указано, возвращает объект города с этим названием.
    :param city_name: НЕ ОБЯЗАТЕЛЬНЫЙ параметр. str(имя города(max_length 20 char)
    :param session: AsyncSession obj
    :returns: list[ResponseCity] если city_name = None, то ResponseCity(Pd obj)
    """
    return await crud.get_all_cities_or_scalar_city(
        city=city_name,
        session=session,
    )


@router.patch(
    path="/update_city/{city_name}",
    response_model=ResponseCity
)
async def update_weather_in_the_city(
        city: str,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер для обновления погоды в указанном городе на текущую.
    :param city: Название города(str)
    :param session: AsyncSession obj
    :returns: ResponseCity >> город, с обновленным состояниеем погоды.
    """
    city_for_update = await crud.get_all_cities_or_scalar_city(
        city=city,
        session=session
    )

    return await crud.update_city_weather(
            city_for_update=city_for_update,
            session=session,
    )


@router.delete(
    path="/delete_city/{city}"
)
async def delete_city(
        city: str,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    """
    Роутер для удаления города. Сначала идет получение объекта города по имени.
    После этот город удаляется из БД.
    :param city: Название города(str)
    :param session: AsyncSession obj
    :returns: None
    """
    city_for_delete = await crud.get_all_cities_or_scalar_city(
        city=city,
        session=session
    )
    await crud.delete_city(
        city_for_delete=city_for_delete,
        session=session
    )
