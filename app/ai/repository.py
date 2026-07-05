from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.models.student_skill import StudentSkill
from app.models.student_domain import StudentDomain

from app.models.fyp_idea import FYPIdea
from app.models.idea_skill import IdeaSkill
from app.models.idea_technology import IdeaTechnology


class AIRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_student(self, user_id):

        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.skills).selectinload(
                    StudentSkill.skill
                ),
                selectinload(Student.domains).selectinload(
                    StudentDomain.domain
                ),
            )
            .where(Student.user_id == user_id)
        )

        return result.scalar_one()

    async def get_all_ideas(self):

        result = await self.db.execute(
            select(FYPIdea)
            .options(
                selectinload(FYPIdea.domain),
                selectinload(FYPIdea.skills).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(FYPIdea.technologies).selectinload(
                    IdeaTechnology.technology
                ),
            )
            .where(FYPIdea.is_active == True)
        )

        return result.scalars().unique().all()