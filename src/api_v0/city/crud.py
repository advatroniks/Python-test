import uuid

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
    city = City(**new_city.model_dump())
    session.add(city)
    await session.commit()

    return city


async def get_all_cities(
        session: AsyncSession
) -> list[City]:
    stmt = select(City)

    cities_seq = await session.scalars(statement=stmt)

    return [city for city in cities_seq]


async def get_all_cities_or_scalar_city(
        session: AsyncSession,
        city: str | None
) -> list[City] | City:

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
    city_for_update.weather = get_weather(city_for_update.name)

    await session.commit()
    return city_for_update


async def delete_city(
        session: AsyncSession,
        city_for_delete: City
):
    await session.delete(city_for_delete)
    await session.commit()
