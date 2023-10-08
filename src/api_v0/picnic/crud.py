import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, attributes
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.api_v0.user.schemas import ResponseUser
from src.models import Picnic, User, PicnicRegistration
from src.api_v0.city.crud import get_city_by_name
from .schemas import CreatePicnic, ResponseAllTournaments


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


async def get_picnics_with_users(
        session: AsyncSession,
        picnic_id: uuid.UUID | None = None,
        picnic_date: datetime | None = None,
        past: bool = True

):
    stmt = (
        select(Picnic)
        .options(
            selectinload(Picnic.picnics_reg)
            .joinedload(PicnicRegistration.user),
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

    total_response = []
    for picnic in picnics_seq_or_instance:
        result = ResponseAllTournaments.model_validate(picnic, from_attributes=True)

        for user in picnic.picnics_reg:
            result.users.append(
                ResponseUser.model_validate(user.user, from_attributes=True)
            )

        total_response.append(result)

    return total_response
