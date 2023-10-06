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


async def get_city_by_name(
        city: str,
        session: AsyncSession,
) -> City:
    stmt = select(City).where(City.name == city)
    result = await session.execute(statement=stmt)
    city: City | None = result.scalar_one_or_none()

    if city is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found in database, try again please!"
        )

    return city


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
