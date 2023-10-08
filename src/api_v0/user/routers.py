from typing import Annotated

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import db_helper
from .schemas import CreateUser, ResponseUser
from . import crud
from .dependences import validate_age_parameter, validate_age_for_add


router = APIRouter(tags=["users"])


@router.post(
    path="/create",
    response_model=ResponseUser
)
async def register_user(
        new_user: CreateUser,
        session: AsyncSession = Depends(db_helper.get_session_dependency)
):
    validate_age_for_add(new_user.age)

    return await crud.create_user(
            session=session,
            new_user=new_user
    )


@router.get(
    path="/get_all"
)
async def get_all_users(
        age_parameters: dict[str, int] = Depends(validate_age_parameter),
        session: AsyncSession = Depends(db_helper.get_session_dependency)

):
    return await crud.get_all_users_or_scalar_user(
        session=session,
        min_age=age_parameters["min_age"],
        max_age=age_parameters["max_age"]
    )


