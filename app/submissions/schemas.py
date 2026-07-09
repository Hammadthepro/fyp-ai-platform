from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubmissionCreate(BaseModel):
    milestone_id: UUID
    github_link: str | None = None
    drive_link: str | None = None
    notes: str | None = None


class SubmissionUpdate(BaseModel):
    status: str
    feedback: str | None = None
    marks: int | None = None


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    milestone_id: UUID
    submitted_by: UUID

    github_link: str | None
    drive_link: str | None
    notes: str | None

    feedback: str | None
    marks: int | None
    status: str

    created_at: datetime
    updated_at: datetime