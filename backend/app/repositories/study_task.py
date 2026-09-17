from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.study_plan import StudyPlan
from app.models.study_task import StudyTask


def create_study_task(
    db: Session,
    study_plan_id: UUID,
    title: str,
    description: str | None,
    scheduled_date: date,
    estimated_minutes: int,
) -> StudyTask:
    study_task = StudyTask(
        study_plan_id=study_plan_id,
        title=title,
        description=description,
        scheduled_date=scheduled_date,
        estimated_minutes=estimated_minutes,
    )

    db.add(study_task)
    db.commit()
    db.refresh(study_task)

    return study_task


def get_study_plan_for_user(
    db: Session,
    study_plan_id: UUID,
    user_id: UUID,
) -> StudyPlan | None:
    statement = select(StudyPlan).where(
        StudyPlan.id == study_plan_id,
        StudyPlan.user_id == user_id,
    )

    return db.execute(statement).scalar_one_or_none()


def get_study_task_for_user(
    db: Session,
    study_task_id: UUID,
    user_id: UUID,
) -> StudyTask | None:
    statement = (
        select(StudyTask)
        .join(StudyPlan, StudyTask.study_plan_id == StudyPlan.id)
        .where(
            StudyTask.id == study_task_id,
            StudyPlan.user_id == user_id,
        )
    )

    return db.execute(statement).scalar_one_or_none()


def list_study_tasks(
    db: Session,
    study_plan_id: UUID,
    user_id: UUID,
) -> list[StudyTask]:
    statement = (
        select(StudyTask)
        .join(StudyPlan, StudyTask.study_plan_id == StudyPlan.id)
        .where(
            StudyTask.study_plan_id == study_plan_id,
            StudyPlan.user_id == user_id,
        )
        .order_by(
            StudyTask.scheduled_date.asc(),
            StudyTask.created_at.asc(),
        )
    )

    return list(db.execute(statement).scalars().all())


def update_study_task(
    db: Session,
    study_task: StudyTask,
    data: dict,
) -> StudyTask:
    for field, value in data.items():
        setattr(study_task, field, value)

    db.commit()
    db.refresh(study_task)

    return study_task


def delete_study_task(
    db: Session,
    study_task: StudyTask,
) -> None:
    db.delete(study_task)
    db.commit()