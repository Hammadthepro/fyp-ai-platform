from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.profile.repository import ProfileRepository
from app.profile.schemas import (
    StudentProfileUpdate,
    ProfessorProfileUpdate,
)


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.repo = ProfileRepository(db)

    # =====================================================
    # STUDENT
    # =====================================================

    async def get_student_profile(self, user):
        student = await self.repo.get_student_by_user_id(user.id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )

        return student

    async def update_student_profile(
        self,
        user,
        data: StudentProfileUpdate,
    ):
        student = await self.repo.get_student_by_user_id(user.id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )

        if data.phone is not None:
            student.phone = data.phone

        if data.github is not None:
            student.github = str(data.github) if data.github else None

        if data.linkedin is not None:
            student.linkedin = str(data.linkedin) if data.linkedin else None

        if data.portfolio is not None:
            student.portfolio = str(data.portfolio) if data.portfolio else None

        await self.repo.update_student()

        if data.skill_ids is not None:
            await self.repo.replace_student_skills(
                student,
                data.skill_ids,
            )

        if data.domain_ids is not None:
            await self.repo.replace_student_domains(
                student,
                data.domain_ids,
            )

        await self.repo.commit()

        return student

    # =====================================================
    # PROFESSOR
    # =====================================================

    async def get_professor_profile(self, user):
        professor = await self.repo.get_professor_by_user_id(
            user.id
        )

        if professor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor profile not found.",
            )

        return professor

    async def update_professor_profile(
        self,
        user,
        data: ProfessorProfileUpdate,
    ):
        professor = await self.repo.get_professor_by_user_id(
            user.id
        )

        if professor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor profile not found.",
            )

        if data.office is not None:
            professor.office = data.office

        if data.bio is not None:
            professor.bio = data.bio

        if data.research_interests is not None:
            professor.research_interests = data.research_interests

        if data.available_slots is not None:
            professor.available_slots = data.available_slots

        await self.repo.update_professor()

        if data.skill_ids is not None:
            await self.repo.replace_professor_skills(
                professor,
                data.skill_ids,
            )

        if data.domain_ids is not None:
            await self.repo.replace_professor_domains(
                professor,
                data.domain_ids,
            )

        await self.repo.commit()

        return professor