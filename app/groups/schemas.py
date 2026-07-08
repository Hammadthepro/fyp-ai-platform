from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
    )


class StudentSimple(BaseModel):
    id: UUID
    registration_number: str
    semester: int

    model_config = {
        "from_attributes": True,
    }


class GroupMemberResponse(BaseModel):
    student: StudentSimple

    model_config = {
        "from_attributes": True,
    }


class GroupResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    members: list[GroupMemberResponse]

    model_config = {
        "from_attributes": True,
    }


class GroupInviteRequest(BaseModel):
    student_id: UUID


class InvitationAction(BaseModel):
    action: str


class InvitationResponse(BaseModel):
    id: UUID
    group_id: UUID
    student_id: UUID
    status: str

    model_config = {
        "from_attributes": True,
    }