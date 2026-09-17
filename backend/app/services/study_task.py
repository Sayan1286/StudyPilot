from uuid import UUID

from sqlalchemy.orm import Session

from app.models.study_task import StudyTask
from app.repositories.study_task import (
    create_study_task,
    delete_study_task,
    get_study_plan_for_user,
    get_study_task_for_user,
    list_study_tasks,
    update_study_task,
)
from app.schemas.study_task import StudyTaskCreate, StudyTaskUpdate


class StudyPlanNotFoundError(Exception):
    pass


class StudyTaskNotFoundError(Exception):
    pass


def create_user_study_task(
    db: Session,
    user_id: UUID,
    study_plan_id: UUID,
    study_task_data: StudyTaskCreate,
) -> StudyTask:
    study_plan = get_study_plan_for_user(
        db=db,
        study_plan_id=study_plan_id,
        user_id=user_id,
    )

    if study_plan is None:
        raise StudyPlanNotFoundError

    return create_study_task(
        db=db,
        study_plan_id=study_plan_id,
        title=study_task_data.title,
        description=study_task_data.description,
        scheduled_date=study_task_data.scheduled_date,
        estimated_minutes=study_task_data.estimated_minutes,
    )


def get_user_study_tasks(
    db: Session,
    user_id: UUID,
    study_plan_id: UUID,
) -> list[StudyTask]:
    study_plan = get_study_plan_for_user(
        db=db,
        study_plan_id=study_plan_id,
        user_id=user_id,
    )

    if study_plan is None:
        raise StudyPlanNotFoundError

    return list_study_tasks(
        db=db,
        study_plan_id=study_plan_id,
        user_id=user_id,
    )


def get_user_study_task(
    db: Session,
    user_id: UUID,
    study_task_id: UUID,
) -> StudyTask:
    study_task = get_study_task_for_user(
        db=db,
        study_task_id=study_task_id,
        user_id=user_id,
    )

    if study_task is None:
        raise StudyTaskNotFoundError

    return study_task


def update_user_study_task(
    db: Session,
    user_id: UUID,
    study_task_id: UUID,
    study_task_data: StudyTaskUpdate,
) -> StudyTask:
    study_task = get_user_study_task(
        db=db,
        user_id=user_id,
        study_task_id=study_task_id,
    )

    update_data = study_task_data.model_dump(exclude_unset=True)

    if not update_data:
        return study_task

    return update_study_task(
        db=db,
        study_task=study_task,
        data=update_data,
    )


def delete_user_study_task(
    db: Session,
    user_id: UUID,
    study_task_id: UUID,
) -> None:
    study_task = get_user_study_task(
        db=db,
        user_id=user_id,
        study_task_id=study_task_id,
    )

    delete_study_task(
        db=db,
        study_task=study_task,
    )