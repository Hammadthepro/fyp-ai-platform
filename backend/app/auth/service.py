from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.enums.roles import UserRole
from app.models.user import User
from app.models.student import Student
from app.models.professor import Professor

from app.schemas.auth import (
    StudentRegister,
    ProfessorRegister,
    LoginRequest,
)


class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthRepository(db)

    async def register_student(
        self,
        data: StudentRegister,
    ):

        existing = await self.repo.get_user_by_email(
            data.email,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        try:

            user = User(
                email=data.email,
                password_hash=hash_password(data.password),
                full_name=data.full_name,
                role=UserRole.STUDENT,
            )

            await self.repo.create_user(user)

            student = Student(
                user_id=user.id,
                registration_number=data.registration_number,
                department=data.department,
                semester=data.semester,
                phone=data.phone,
            )

            await self.repo.create_student(student)

            await self.repo.commit()

            token = create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "role": user.role.value,
                }
            )

            return {
                "access_token": token,
                "token_type": "bearer",
            }

        except Exception:
            await self.repo.rollback()
            raise

    async def register_professor(
        self,
        data: ProfessorRegister,
    ):

        existing = await self.repo.get_user_by_email(
            data.email,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        try:

            user = User(
                email=data.email,
                password_hash=hash_password(data.password),
                full_name=data.full_name,
                role=UserRole.PROFESSOR,
            )

            await self.repo.create_user(user)

            professor = Professor(
                user_id=user.id,
                employee_id=data.employee_id,
                designation=data.designation,
                office=data.office,
                bio=data.bio,
                research_interests=data.research_interests,
                max_groups=data.max_groups,
                available_slots=data.max_groups,
            )

            await self.repo.create_professor(
                professor,
            )

            await self.repo.commit()

            token = create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "role": user.role.value,
                }
            )

            return {
                "access_token": token,
                "token_type": "bearer",
            }

        except Exception:
            await self.repo.rollback()
            raise

    async def login(
        self,
        data: LoginRequest,
    ):

        user = await self.repo.get_user_by_email(
            data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive.",
            )

        user.last_login = datetime.now(
            timezone.utc,
        )

        await self.repo.update_user(user)
        await self.repo.commit()

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }