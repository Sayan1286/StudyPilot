# ruff: noqa: B008

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.study_task import (
    StudyTaskCreate,
    StudyTaskResponse,
    StudyTaskUpdate,
)
from app.services.study_task import (
    StudyPlanNotFoundError,
    StudyTaskNotFoundError,
    create_user_study_task,
    delete_user_study_task,
    get_user_study_task,
    get_user_study_tasks,
    update_user_study_task,
)

router = APIRouter(
    prefix="/study-plans/{study_plan_id}/tasks",
    tags=["Study Tasks"],
)


@router.post(
    "",
    response_model=StudyTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_task_route(
    study_plan_id: UUID,
    study_task_data: StudyTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyTaskResponse:
    try:
        study_task = create_user_study_task(
            db=db,
            user_id=current_user.id,
            study_plan_id=study_plan_id,
            study_task_data=study_task_data,
        )
    except StudyPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found",
        )

    return StudyTaskResponse.model_validate(study_task)


@router.get(
    "",
    response_model=list[StudyTaskResponse],
)
def list_study_tasks_route(
    study_plan_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[StudyTaskResponse]:
    try:
        study_tasks = get_user_study_tasks(
            db=db,
            user_id=current_user.id,
            study_plan_id=study_plan_id,
        )
    except StudyPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study plan not found",
        )

    return [
        StudyTaskResponse.model_validate(study_task)
        for study_task in study_tasks
    ]


@router.get(
    "/{study_task_id}",
    response_model=StudyTaskResponse,
)
def get_study_task_route(
    study_task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyTaskResponse:
    try:
        study_task = get_user_study_task(
            db=db,
            user_id=current_user.id,
            study_task_id=study_task_id,
        )
    except StudyTaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )

    return StudyTaskResponse.model_validate(study_task)


@router.put(
    "/{study_task_id}",
    response_model=StudyTaskResponse,
)
def update_study_task_route(
    study_task_id: UUID,
    study_task_data: StudyTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudyTaskResponse:
    try:
        study_task = update_user_study_task(
            db=db,
            user_id=current_user.id,
            study_task_id=study_task_id,
            study_task_data=study_task_data,
        )
    except StudyTaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )

    return StudyTaskResponse.model_validate(study_task)


@router.delete(
    "/{study_task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study_task_route(
    study_task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    try:
        delete_user_study_task(
            db=db,
            user_id=current_user.id,
            study_task_id=study_task_id,
        )
    except StudyTaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study task not found",
        )