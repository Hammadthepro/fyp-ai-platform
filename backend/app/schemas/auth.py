from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID

class StudentRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str

    registration_number: str
    department: str
    semester: int
    phone: str | None = None


class ProfessorRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str

    employee_id: str
    designation: str
    office: str | None = None
    bio: str | None = None
    research_interests: str | None = None

    max_groups: int = 10


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    is_verified: bool