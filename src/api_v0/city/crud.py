from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select

from fastapi import HTTPException, status

from src.models import City
from .schemas import CreateCity
from .weather.weather_get import get_weather


async def create_city(
        new_city: CreateCity,
        session: AsyncSession
) -> City:
    """
    Функция принимает async_session object и CreateCity(pydantic object).
    Добавляет в бд новый город.
    :param new_city: Объект pydantic(CreateCity)
    :param session: AsyncSession object
    :returns: City (созданный город)
    """
    city = City(**new_city.model_dump())
    session.add(city)
    await session.commit()

    return city


async def get_all_cities_or_scalar_city(
        session: AsyncSession,
        city: str | None
) -> list[City] | City:
    """
    Если функция принимает имя города, при наличии его в БД возвращает объект City.
    Если же параметр city=None, то функция возвращает список из всех объектов City.
    :param session: AsyncSession object
    :param city: str(city_name) | None
    :returns: list[City] | City |
    :raises HTTPException: HTTP_404_NOT_FOUND, если в БД нет ни одного города или нет соответствия
    по входящему параметру city(city_name)
    """
    stmt = select(City)
    if city:
        stmt = stmt.where(City.name == city)

    cities = await session.execute(statement=stmt)
    cities_seq = cities.scalars().all()

    if not cities_seq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City(s) not found in database, try again please!"
        )
    if len(cities_seq) == 1:
        return cities_seq[0]
    return [city for city in cities_seq]


async def update_city_weather(
        session: AsyncSession,
        city_for_update: City
) -> City:
    """
    Функция принимает City object. Запрашивает актуальную на данный момент погоду для
    этого города.
    :param session: AsyncSession object.
    :param city_for_update: City object, объект города для обновления.
    :returns: city_for_update City object, с обновленными данными погоды.
    """
    city_for_update.weather = get_weather(city_for_update.name)

    await session.commit()
    return city_for_update


async def delete_city(
        session: AsyncSession,
        city_for_delete: City
):
    """
    Функция принимает City object, и удаляет его из бд.
    :param session: AsyncSession object.
    :param city_for_delete: City object, город для удаления.
    :returns: None
    """
    await session.delete(city_for_delete)
    await session.commit()
