from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from .schemas import CreateUser, ResponseUser
from . import crud


router = APIRouter(tags=["users"])


@router.post(
    path="/create",
    response_model=ResponseUser
)
async def register_user(
        new_user: CreateUser,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    return await crud.create_user(
            session=session,
            new_user=new_user
    )
