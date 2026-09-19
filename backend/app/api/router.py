from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.study_plan_generation import (
    router as study_plan_generation_router,
)
from app.api.routes.study_plans import router as study_plans_router
from app.api.routes.study_tasks import router as study_tasks_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(study_plans_router)
api_router.include_router(study_tasks_router)
api_router.include_router(study_plan_generation_router)