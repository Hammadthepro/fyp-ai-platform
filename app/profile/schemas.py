from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class StudentProfileUpdate(BaseModel):
    phone: str | None = None
    github: HttpUrl | None = None
    linkedin: HttpUrl | None = None
    portfolio: HttpUrl | None = None

    skill_ids: list[UUID] = []
    domain_ids: list[UUID] = []


class ProfessorProfileUpdate(BaseModel):
    office: str | None = None
    bio: str | None = None
    research_interests: str | None = None
    available_slots: int | None = None

    skill_ids: list[UUID] = []
    domain_ids: list[UUID] = []


class StudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    registration_number: str
    department: str
    semester: int
    phone: str | None
    github: str | None
    linkedin: str | None
    portfolio: str | None


class ProfessorProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: str
    designation: str
    office: str | None
    bio: str | None
    research_interests: str | None
    available_slots: int