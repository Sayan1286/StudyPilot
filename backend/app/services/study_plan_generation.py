from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.study_plan import StudyPlan
from app.models.study_task import StudyTask
from app.schemas.study_plan_generation import (
    GeneratedTask,
    StudyPlanGenerationRequest,
    StudyPlanGenerationResponse,
)


class StudyPlanGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        request: StudyPlanGenerationRequest,
    ) -> StudyPlanGenerationResponse:
        """Generate a study plan from the supplied request."""
        raise NotImplementedError


class LocalStudyPlanGenerator(StudyPlanGenerator):
    def generate(
        self,
        request: StudyPlanGenerationRequest,
    ) -> StudyPlanGenerationResponse:
        from datetime import timedelta

        study_days = (request.end_date - request.start_date).days + 1
        daily_minutes = round(request.available_hours_per_day * 60)

        tasks: list[GeneratedTask] = []

        for day_number in range(study_days):
            scheduled_date = request.start_date + timedelta(days=day_number)

            tasks.append(
                GeneratedTask(
                    title=f"Study {request.subject} - Day {day_number + 1}",
                    description=(
                        f"Work toward the goal: {request.goal}"
                    ),
                    scheduled_date=scheduled_date,
                    estimated_minutes=daily_minutes,
                )
            )

        return StudyPlanGenerationResponse(
            title=f"{request.subject} Study Plan",
            subject=request.subject,
            goal=request.goal,
            start_date=request.start_date,
            end_date=request.end_date,
            daily_hours=request.available_hours_per_day,
            tasks=tasks,
        )


class AIStudyPlanGenerator(StudyPlanGenerator):
    def generate(
        self,
        request: StudyPlanGenerationRequest,
    ) -> StudyPlanGenerationResponse:
        raise NotImplementedError(
            "AI study plan generation is not configured yet"
        )


def generate_and_save_study_plan(
    db: Session,
    user_id,
    request: StudyPlanGenerationRequest,
) -> StudyPlanGenerationResponse:
    generator = LocalStudyPlanGenerator()
    generated_plan = generator.generate(request)

    try:
        study_plan = StudyPlan(
            user_id=user_id,
            title=generated_plan.title,
            subject=generated_plan.subject,
            goal=generated_plan.goal,
            start_date=generated_plan.start_date,
            end_date=generated_plan.end_date,
            daily_hours=generated_plan.daily_hours,
        )

        db.add(study_plan)
        db.flush()

        study_tasks = [
            StudyTask(
                study_plan_id=study_plan.id,
                title=task.title,
                description=task.description,
                scheduled_date=task.scheduled_date,
                estimated_minutes=task.estimated_minutes,
            )
            for task in generated_plan.tasks
        ]

        db.add_all(study_tasks)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return generated_plan