from datetime import date

from pydantic import BaseModel, Field, model_validator


class StudyPlanGenerationRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=150)
    goal: str = Field(min_length=1, max_length=1000)
    available_hours_per_day: float = Field(gt=0, le=24)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_generation_request(self) -> "StudyPlanGenerationRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")

        study_days = (self.end_date - self.start_date).days + 1

        if study_days > 365:
            raise ValueError("study period cannot exceed 365 days")

        return self


class GeneratedTask(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    scheduled_date: date
    estimated_minutes: int = Field(gt=0, le=1440)


class StudyPlanGenerationResponse(BaseModel):
    title: str
    subject: str
    goal: str
    start_date: date
    end_date: date
    daily_hours: float
    tasks: list[GeneratedTask]