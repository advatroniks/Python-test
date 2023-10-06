from fastapi import APIRouter

from .city.routes import router as city_router


router = APIRouter()

router.include_router(router=city_router, prefix="/city")