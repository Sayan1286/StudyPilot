# ruff: noqa: B008
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudyPlanUpdate,
)
from app.services.study_plan import (
    InvalidStudyPlanDatesError,
    StudyPlanNotFoundError,
    create_user_study_plan,
    delete_user_study_plan,
    get_user_study_plan,
    get_user_study_plans,
    update_user_study_plan,
)

router = APIRouter(
    prefix="/study-plans",
    tags=["Study Plans"],
)


@router.post(
    "",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_plan_route(
    study_plan_data: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyPlanResponse:
    study_plan = create_user_study_plan(
        db=db,
        user_id=current_user.id,
        study_plan_data=study_plan_data,
    )

    return StudyPlanResponse.model_validate(study_plan)


@router.get(
    "",
    response_model=list[StudyPlanResponse],
)
def list_study_plans_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[StudyPlanResponse]:
    study_plans = get_user_study_plans(
        db=db,
        user_id=current_user.id,
    )

    return [
        StudyPlanResponse.model_validate(study_plan)
        for study_plan in study_plans
    ]


@router.get(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def get_study_plan_route(
    study_plan_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyPlanResponse:
    try:
        study_plan = get_user_study_plan(
            db=db,
            user_id=current_user.id,
            study_plan_id=study_plan_id,
        )
    except StudyPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found",
        )

    return StudyPlanResponse.model_validate(study_plan)


@router.put(
    "/{study_plan_id}",
    response_model=StudyPlanResponse,
)
def update_study_plan_route(
    study_plan_id: UUID,
    study_plan_data: StudyPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyPlanResponse:
    try:
        study_plan = update_user_study_plan(
            db=db,
            user_id=current_user.id,
            study_plan_id=study_plan_id,
            study_plan_data=study_plan_data,
        )
    except StudyPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found",
        )
    except InvalidStudyPlanDatesError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must be on or after start_date",
        )

    return StudyPlanResponse.model_validate(study_plan)


@router.delete(
    "/{study_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study_plan_route(
    study_plan_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    try:
        delete_user_study_plan(
            db=db,
            user_id=current_user.id,
            study_plan_id=study_plan_id,
        )
    except StudyPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found",
        )