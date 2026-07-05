from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import Domain
from app.models.fyp_idea import FYPIdea
from app.models.idea_skill import IdeaSkill
from app.models.idea_technology import IdeaTechnology
from app.models.professor import Professor
from app.models.skill import Skill
from app.models.technology import Technology
from app.models.user import User


class IdeaRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ----------------------------
    # Helpers
    # ----------------------------

    async def get_professor_by_user(self, user_id: UUID):
        result = await self.db.execute(
            select(Professor).where(
                Professor.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_domain(self, domain_id: UUID):
        return await self.db.get(Domain, domain_id)

    async def get_skills(self, ids: list[UUID]):
        if not ids:
            return []

        result = await self.db.execute(
            select(Skill).where(Skill.id.in_(ids))
        )

        return result.scalars().all()

    async def get_technologies(self, ids: list[UUID]):
        if not ids:
            return []

        result = await self.db.execute(
            select(Technology).where(
                Technology.id.in_(ids)
            )
        )

        return result.scalars().all()

    # ----------------------------
    # CRUD
    # ----------------------------

    async def create(self, idea: FYPIdea):
        self.db.add(idea)
        await self.db.flush()
        await self.db.refresh(idea)
        return idea

    async def get_by_id(self, idea_id: UUID):
        result = await self.db.execute(
            select(FYPIdea)
            .where(FYPIdea.id == idea_id)
            .options(
                selectinload(FYPIdea.domain),
                selectinload(FYPIdea.skills).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(FYPIdea.technologies).selectinload(
                    IdeaTechnology.technology
                ),
                selectinload(FYPIdea.professor).selectinload(
                    Professor.user
                ),
            )
        )

        return result.scalar_one_or_none()

    async def get_professor_idea(
        self,
        professor_id: UUID,
        idea_id: UUID,
    ):
        result = await self.db.execute(
            select(FYPIdea)
            .where(
                FYPIdea.id == idea_id,
                FYPIdea.professor_id == professor_id,
            )
            .options(
                selectinload(FYPIdea.domain),
                selectinload(FYPIdea.skills).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(FYPIdea.technologies).selectinload(
                    IdeaTechnology.technology
                ),
                selectinload(FYPIdea.professor).selectinload(
                    Professor.user
                ),
            )
        )

        return result.scalar_one_or_none()

    async def get_professor_ideas(
        self,
        professor_id: UUID,
    ):
        result = await self.db.execute(
            select(FYPIdea)
            .where(
                FYPIdea.professor_id == professor_id
            )
            .order_by(
                FYPIdea.created_at.desc()
            )
            .options(
                selectinload(FYPIdea.domain),
                selectinload(FYPIdea.skills).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(FYPIdea.technologies).selectinload(
                    IdeaTechnology.technology
                ),
                selectinload(FYPIdea.professor).selectinload(
                    Professor.user
                ),
            )
        )

        return result.scalars().unique().all()

    async def delete(self, idea: FYPIdea):
        await self.db.delete(idea)

    # ----------------------------
    # Relations
    # ----------------------------

    async def replace_skills(
        self,
        idea_id: UUID,
        skill_ids: list[UUID],
    ):
        await self.db.execute(
            delete(IdeaSkill).where(
                IdeaSkill.idea_id == idea_id
            )
        )

        for skill_id in skill_ids:
            self.db.add(
                IdeaSkill(
                    idea_id=idea_id,
                    skill_id=skill_id,
                )
            )

    async def replace_technologies(
        self,
        idea_id: UUID,
        technology_ids: list[UUID],
    ):
        await self.db.execute(
            delete(IdeaTechnology).where(
                IdeaTechnology.idea_id == idea_id
            )
        )

        for technology_id in technology_ids:
            self.db.add(
                IdeaTechnology(
                    idea_id=idea_id,
                    technology_id=technology_id,
                )
            )

    # ----------------------------
    # Public Idea Listing
    # ----------------------------

    async def list_ideas(
        self,
        keyword: str | None = None,
        domain_id: UUID | None = None,
        difficulty: str | None = None,
        technology_id: UUID | None = None,
        skill_id: UUID | None = None,
        professor: str | None = None,
        newest: bool = True,
    ):
        query = (
            select(FYPIdea)
            .options(
                selectinload(FYPIdea.domain),
                selectinload(FYPIdea.skills).selectinload(
                    IdeaSkill.skill
                ),
                selectinload(FYPIdea.technologies).selectinload(
                    IdeaTechnology.technology
                ),
                selectinload(FYPIdea.professor).selectinload(
                    Professor.user
                ),
            )
            .where(FYPIdea.is_active.is_(True))
        )

        if keyword:
            query = query.where(
                or_(
                    FYPIdea.title.ilike(f"%{keyword}%"),
                    FYPIdea.description.ilike(f"%{keyword}%"),
                )
            )

        if domain_id:
            query = query.where(
                FYPIdea.domain_id == domain_id
            )

        if difficulty:
            query = query.where(
                FYPIdea.difficulty == difficulty
            )

        if technology_id:
            query = query.join(IdeaTechnology).where(
                IdeaTechnology.technology_id == technology_id
            )

        if skill_id:
            query = query.join(IdeaSkill).where(
                IdeaSkill.skill_id == skill_id
            )

        if professor:
            query = (
                query.join(Professor)
                .join(User)
                .where(
                    User.full_name.ilike(f"%{professor}%")
                )
            )

        query = query.order_by(
            FYPIdea.created_at.desc()
            if newest
            else FYPIdea.created_at.asc()
        )

        result = await self.db.execute(query)

        return result.scalars().unique().all()