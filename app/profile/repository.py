from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.models.professor import Professor
from app.models.student_skill import StudentSkill
from app.models.student_domain import StudentDomain
from app.models.professor_skill import ProfessorSkill
from app.models.professor_domain import ProfessorDomain


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================================================
    # STUDENT
    # ======================================================

    async def get_student_by_user_id(self, user_id):
        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.skills),
                selectinload(Student.domains),
            )
            .where(Student.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def update_student(self):
        await self.db.flush()

    async def replace_student_skills(
        self,
        student: Student,
        skill_ids: list,
    ):
        student.skills.clear()

        for skill_id in skill_ids:
            student.skills.append(
                StudentSkill(
                    skill_id=skill_id,
                )
            )

        await self.db.flush()

    async def replace_student_domains(
        self,
        student: Student,
        domain_ids: list,
    ):
        student.domains.clear()

        for domain_id in domain_ids:
            student.domains.append(
                StudentDomain(
                    domain_id=domain_id,
                )
            )

        await self.db.flush()

    # ======================================================
    # PROFESSOR
    # ======================================================

    async def get_professor_by_user_id(
        self,
        user_id,
    ):
        result = await self.db.execute(
            select(Professor)
            .options(
                selectinload(Professor.skills),
                selectinload(Professor.domains),
            )
            .where(
                Professor.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def update_professor(self):
        await self.db.flush()

    async def replace_professor_skills(
        self,
        professor: Professor,
        skill_ids: list,
    ):
        professor.skills.clear()

        for skill_id in skill_ids:
            professor.skills.append(
                ProfessorSkill(
                    skill_id=skill_id,
                )
            )

        await self.db.flush()

    async def replace_professor_domains(
        self,
        professor: Professor,
        domain_ids: list,
    ):
        professor.domains.clear()

        for domain_id in domain_ids:
            professor.domains.append(
                ProfessorDomain(
                    domain_id=domain_id,
                )
            )

        await self.db.flush()

    # ======================================================
    # SAVE
    # ======================================================

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()