from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.study_plans import router as study_plans_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(study_plans_router)