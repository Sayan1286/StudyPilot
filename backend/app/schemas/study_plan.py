from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StudyPlanCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    subject: str = Field(min_length=1, max_length=150)
    goal: str = Field(min_length=1)
    start_date: date
    end_date: date
    daily_hours: float = Field(gt=0, le=24)

    @model_validator(mode="after")
    def validate_dates(self) -> "StudyPlanCreate":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class StudyPlanUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    subject: str | None = Field(default=None, min_length=1, max_length=150)
    goal: str | None = Field(default=None, min_length=1)
    start_date: date | None = None
    end_date: date | None = None
    daily_hours: float | None = Field(default=None, gt=0, le=24)

    @model_validator(mode="after")
    def validate_dates(self) -> "StudyPlanUpdate":
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("end_date must be on or after start_date")
        return self


class StudyPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    subject: str
    goal: str
    start_date: date
    end_date: date
    daily_hours: float
    status: str
    created_at: datetime
    updated_at: datetime