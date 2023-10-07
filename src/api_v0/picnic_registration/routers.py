import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from src.api_v0.user.crud import get_user_by_id
from src.api_v0.picnic.crud import get_picnic_by_id

from .service import check_actual_date
from .schemas import RegistrationUserPicnic, RegistrationUserResponse
from . import crud


router = APIRouter(
    tags=["registration_picnic"]
)


@router.post(
    path="/registration_for_picnic",
    response_model=RegistrationUserResponse
)
async def registration_for_picnic(
        picnic_registration: RegistrationUserPicnic,
        session: AsyncSession = Depends(db_helper.get_session_dependency),
):
    picnic = await get_picnic_by_id(
        session=session,
        picnic_id=picnic_registration.picnic_id

    )

    check_actual_date(picnic.time)

    user = await get_user_by_id(
        session=session,
        user_id=picnic_registration.user_id
    )

    return await crud.add_user_for_registration_picnic(
        new_registration=picnic_registration,
        session=session
    )




