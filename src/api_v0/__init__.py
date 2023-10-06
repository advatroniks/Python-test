from fastapi import APIRouter

from .city.routes import router as city_router
from .picnic.routers import router as picnic_router
from .user.routers import router as user_router

router = APIRouter()

router.include_router(router=city_router, prefix="/city")
router.include_router(router=picnic_router, prefix="/picnic")
router.include_router(router=user_router, prefix="/user")