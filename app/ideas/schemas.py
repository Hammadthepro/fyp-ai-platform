from uuid import UUID

from pydantic import BaseModel, Field


# ----------------------------------
# Create / Update
# ----------------------------------

class IdeaCreate(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=255,
    )

    description: str = Field(
        min_length=20,
    )

    domain_id: UUID

    difficulty: str = Field(
        default="Intermediate",
    )

    max_students: int = Field(
        default=3,
        ge=1,
        le=5,
    )

    technology_ids: list[UUID] = []

    skill_ids: list[UUID] = []


class IdeaUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=5,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=20,
    )

    domain_id: UUID | None = None

    difficulty: str | None = None

    max_students: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    technology_ids: list[UUID] | None = None

    skill_ids: list[UUID] | None = None

    is_active: bool | None = None


# ----------------------------------
# Nested Response Models
# ----------------------------------

class DomainSimple(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }


class SkillSimple(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }


class TechnologySimple(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }


class IdeaSkillResponse(BaseModel):
    skill: SkillSimple

    model_config = {
        "from_attributes": True,
    }


class IdeaTechnologyResponse(BaseModel):
    technology: TechnologySimple

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------
# API Response
# ----------------------------------

class IdeaResponse(BaseModel):
    id: UUID

    title: str

    description: str

    difficulty: str

    max_students: int

    is_active: bool

    created_at: str

    domain: DomainSimple

    skills: list[IdeaSkillResponse]

    technologies: list[IdeaTechnologyResponse]

    model_config = {
        "from_attributes": True,
    }