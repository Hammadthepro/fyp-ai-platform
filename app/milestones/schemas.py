from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MilestoneCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str

    due_date: datetime


class MilestoneUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    status: str | None = None
    feedback: str | None = None


class MilestoneResponse(BaseModel):
    id: UUID
    group_id: UUID

    title: str
    description: str

    due_date: datetime

    status: str
    feedback: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }