from uuid import UUID

from pydantic import BaseModel, Field


class SkillCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class SkillResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }


class DomainCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class DomainResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }


class TechnologyCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class TechnologyResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }