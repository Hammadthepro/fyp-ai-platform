from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.permissions import require_role
from app.database.database import get_db
from app.enums.roles import UserRole
from app.models.user import User
from app.profile.service import ProfileService
from app.profile.schemas import (
    StudentProfileResponse,
    ProfessorProfileResponse,
    StudentProfileUpdate,
    ProfessorProfileUpdate,
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


# ==========================================================
# STUDENT
# ==========================================================

@router.get(
    "/student",
    response_model=StudentProfileResponse,
)
async def get_student_profile(
    current_user: User = Depends(
        require_role(UserRole.STUDENT)
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)
    return await service.get_student_profile(current_user)


@router.put(
    "/student",
    response_model=StudentProfileResponse,
)
async def update_student_profile(
    data: StudentProfileUpdate,
    current_user: User = Depends(
        require_role(UserRole.STUDENT)
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)

    return await service.update_student_profile(
        current_user,
        data,
    )


# ==========================================================
# PROFESSOR
# ==========================================================

@router.get(
    "/professor",
    response_model=ProfessorProfileResponse,
)
async def get_professor_profile(
    current_user: User = Depends(
        require_role(UserRole.PROFESSOR)
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)

    return await service.get_professor_profile(
        current_user,
    )


@router.put(
    "/professor",
    response_model=ProfessorProfileResponse,
)
async def update_professor_profile(
    data: ProfessorProfileUpdate,
    current_user: User = Depends(
        require_role(UserRole.PROFESSOR)
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ProfileService(db)

    return await service.update_professor_profile(
        current_user,
        data,
    )