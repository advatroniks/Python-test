import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException, status

from src.models import Picnic
from src.api_v0.city.crud import get_city_by_name
from .schemas import CreatePicnic


async def create_picnic(
        picnic: CreatePicnic,
        session: AsyncSession,
):
    city = await get_city_by_name(
        city=picnic.city_name,
        session=session
    )
    print(city.id, picnic.time)
    new_picnic = Picnic(
        city_id=city.id,
        time=picnic.time,
    )
    session.add(new_picnic)
    await session.commit()

    return new_picnic


async def get_all_picnics(
        session: AsyncSession
):
    stmt = select(Picnic)
    result = await session.execute(statement=stmt)
    picnics = result.scalars()

    return picnics


async def get_picnic_by_id(
        session: AsyncSession,
        picnic_id: uuid.UUID
) -> Picnic:
    stmt = select(Picnic).where(Picnic.id == picnic_id)
    result = await session.execute(statement=stmt)
    picnic = result.scalar_one_or_none()

    if picnic is None:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picnic can not found, check picnic id"
        )

    return picnic



