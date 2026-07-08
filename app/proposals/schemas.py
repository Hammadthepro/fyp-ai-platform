from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class ProposalCreate(BaseModel):
    professor_id: UUID

    title: str = Field(
        min_length=5,
        max_length=255,
    )

    abstract: str = Field(
        min_length=20,
    )

    objectives: str = Field(
        min_length=10,
    )


class ProposalResponse(BaseModel):
    id: UUID

    group_id: UUID
    professor_id: UUID

    title: str
    abstract: str
    objectives: str

    status: str
    feedback: str | None = None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ProposalReview(BaseModel):
    action: str
    feedback: str | None = None