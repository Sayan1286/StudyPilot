# ruff: noqa: B008

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.study_plan_generation import (
    StudyPlanGenerationRequest,
    StudyPlanGenerationResponse,
)
from app.services.study_plan_generation import LocalStudyPlanGenerator

router = APIRouter(
    prefix="/study-plans",
    tags=["Study Plan Generation"],
)


@router.post(
    "/generate",
    response_model=StudyPlanGenerationResponse,
)
def generate_study_plan(
    request: StudyPlanGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyPlanGenerationResponse:
    generator = LocalStudyPlanGenerator()
    return generator.generate(request)