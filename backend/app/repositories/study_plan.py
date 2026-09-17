from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.study_plan import StudyPlan


def create_study_plan(
    db: Session,
    user_id: UUID,
    title: str,
    subject: str,
    goal: str,
    start_date: date,
    end_date: date,
    daily_hours: float,
) -> StudyPlan:
    study_plan = StudyPlan(
        user_id=user_id,
        title=title,
        subject=subject,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
        daily_hours=daily_hours,
    )

    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)

    return study_plan


def get_study_plan(
    db: Session,
    study_plan_id: UUID,
    user_id: UUID,
) -> StudyPlan | None:
    statement = select(StudyPlan).where(
        StudyPlan.id == study_plan_id,
        StudyPlan.user_id == user_id,
    )

    return db.execute(statement).scalar_one_or_none()


def list_study_plans(
    db: Session,
    user_id: UUID,
) -> list[StudyPlan]:
    statement = (
        select(StudyPlan)
        .where(StudyPlan.user_id == user_id)
        .order_by(StudyPlan.created_at.desc())
    )

    return list(db.execute(statement).scalars().all())


def update_study_plan(
    db: Session,
    study_plan: StudyPlan,
    data: dict,
) -> StudyPlan:
    for field, value in data.items():
        setattr(study_plan, field, value)

    db.commit()
    db.refresh(study_plan)

    return study_plan


def delete_study_plan(
    db: Session,
    study_plan: StudyPlan,
) -> None:
    db.delete(study_plan)
    db.commit()