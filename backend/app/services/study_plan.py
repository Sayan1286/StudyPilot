
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.study_plan import StudyPlan
from app.repositories.study_plan import (
    create_study_plan,
    delete_study_plan,
    get_study_plan,
    list_study_plans,
    update_study_plan,
)
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate


class StudyPlanNotFoundError(Exception):
    pass


class InvalidStudyPlanDatesError(Exception):
    pass


def create_user_study_plan(
    db: Session,
    user_id: UUID,
    study_plan_data: StudyPlanCreate,
) -> StudyPlan:
    return create_study_plan(
        db=db,
        user_id=user_id,
        title=study_plan_data.title,
        subject=study_plan_data.subject,
        goal=study_plan_data.goal,
        start_date=study_plan_data.start_date,
        end_date=study_plan_data.end_date,
        daily_hours=study_plan_data.daily_hours,
    )


def get_user_study_plan(
    db: Session,
    user_id: UUID,
    study_plan_id: UUID,
) -> StudyPlan:
    study_plan = get_study_plan(
        db=db,
        study_plan_id=study_plan_id,
        user_id=user_id,
    )

    if study_plan is None:
        raise StudyPlanNotFoundError

    return study_plan


def get_user_study_plans(
    db: Session,
    user_id: UUID,
) -> list[StudyPlan]:
    return list_study_plans(
        db=db,
        user_id=user_id,
    )


def update_user_study_plan(
    db: Session,
    user_id: UUID,
    study_plan_id: UUID,
    study_plan_data: StudyPlanUpdate,
) -> StudyPlan:
    study_plan = get_user_study_plan(
        db=db,
        user_id=user_id,
        study_plan_id=study_plan_id,
    )

    update_data = study_plan_data.model_dump(exclude_unset=True)

    new_start_date = update_data.get("start_date", study_plan.start_date)
    new_end_date = update_data.get("end_date", study_plan.end_date)

    if new_end_date < new_start_date:
        raise InvalidStudyPlanDatesError

    if not update_data:
        return study_plan

    return update_study_plan(
        db=db,
        study_plan=study_plan,
        data=update_data,
    )


def delete_user_study_plan(
    db: Session,
    user_id: UUID,
    study_plan_id: UUID,
) -> None:
    study_plan = get_user_study_plan(
        db=db,
        user_id=user_id,
        study_plan_id=study_plan_id,
    )

    delete_study_plan(
        db=db,
        study_plan=study_plan,
    )