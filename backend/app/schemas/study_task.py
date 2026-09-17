from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StudyTaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    scheduled_date: date
    estimated_minutes: int = Field(gt=0, le=1440)


class StudyTaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    scheduled_date: date | None = None
    estimated_minutes: int | None = Field(default=None, gt=0, le=1440)
    status: str | None = Field(default=None, min_length=1, max_length=20)


class StudyTaskStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=20)


class StudyTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    study_plan_id: UUID
    title: str
    description: str | None
    scheduled_date: date
    estimated_minutes: int
    status: str
    created_at: datetime
    updated_at: datetime