from abc import ABC, abstractmethod
from datetime import timedelta

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