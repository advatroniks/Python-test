from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends


from src.models import db_helper
from .schemas import CreatePicnic
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


