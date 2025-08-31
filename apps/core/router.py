from fastapi import APIRouter

from apps.bonus_system.route import router as bonus_system_router  # <-- импорт объекта


router = APIRouter(prefix="/api")

v1 = APIRouter(prefix="/v1")
v1.include_router(bonus_system_router, prefix="/bonus-system", tags=["bonus-system"])

router.include_router(v1)
