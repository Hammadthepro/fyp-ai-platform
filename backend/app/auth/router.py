from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.core.dependencies import get_current_user
from app.core.permissions import require_role
from app.database.database import get_db
from app.enums.roles import UserRole
from app.models.user import User
from app.schemas.auth import (
    StudentRegister,
    ProfessorRegister,
    TokenResponse,
    LoginRequest,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register/student",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_student(
    data: StudentRegister,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.register_student(data)


@router.post(
    "/register/professor",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_professor(
    data: ProfessorRegister,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.register_professor(data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    login_data = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    return await service.login(login_data)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/professor-only")
async def professor_only(
    current_user: User = Depends(
        require_role(UserRole.PROFESSOR)
    ),
):
    return {
        "message": f"Welcome Professor {current_user.full_name}"
    }