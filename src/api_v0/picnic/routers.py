import uuid
from datetime import datetime

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Query


from src.models import db_helper
from .schemas import CreatePicnic, ResponseAllTournaments
from . import crud

router = APIRouter(
    tags=["picnics"]
)


@router.post(
    path="/create_picnic"
)
async def create_picnic(
        picnic: CreatePicnic,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    return await crud.create_picnic(
        picnic=picnic,
        session=session
    )


@router.get(
    path="/all_picnics",
    response_model=list[ResponseAllTournaments]
)
async def get_all_picnics_with_users(
        date_time: Annotated[
            datetime | None,
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

    return await crud.get_picnics_with_users(
        session=session,
        past=past,
        picnic_date=date_time
    )


@router.get(
    path="/picnic{picnic_id}"
)
async def get_picnic_with_users_by_id(
        picnic_id: uuid.UUID,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    return await crud.get_picnics_with_users(
        session=session,
        picnic_id=picnic_id
    )
