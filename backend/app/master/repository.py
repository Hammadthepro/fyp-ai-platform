from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.technology import Technology
from app.models.domain import Domain
from app.models.skill import Skill


class MasterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------- Skills ----------

    async def get_all_skills(self):
        result = await self.db.execute(
            select(Skill).order_by(Skill.name)
        )
        return result.scalars().all()

    async def search_skills(self, query: str):
        result = await self.db.execute(
            select(Skill)
            .where(
                func.lower(Skill.name).contains(
                    query.lower()
                )
            )
            .order_by(Skill.name)
        )
        return result.scalars().all()

    async def get_skill_by_name(self, name: str):
        result = await self.db.execute(
            select(Skill).where(
                func.lower(Skill.name)
                == name.lower()
            )
        )
        return result.scalar_one_or_none()

    async def create_skill(self, name: str):
        skill = Skill(name=name)

        self.db.add(skill)

        await self.db.flush()
        await self.db.refresh(skill)

        return skill

    # ---------- Domains ----------

    async def get_all_domains(self):
        result = await self.db.execute(
            select(Domain).order_by(Domain.name)
        )
        return result.scalars().all()

    async def search_domains(self, query: str):
        result = await self.db.execute(
            select(Domain)
            .where(
                func.lower(Domain.name).contains(
                    query.lower()
                )
            )
            .order_by(Domain.name)
        )
        return result.scalars().all()

    async def get_domain_by_name(self, name: str):
        result = await self.db.execute(
            select(Domain).where(
                func.lower(Domain.name)
                == name.lower()
            )
        )
        return result.scalar_one_or_none()

    async def create_domain(self, name: str):
        domain = Domain(name=name)

        self.db.add(domain)

        await self.db.flush()
        await self.db.refresh(domain)

        return domain


        # ---------- Technologies ----------

    async def get_all_technologies(self):
        result = await self.db.execute(
            select(Technology).order_by(Technology.name)
        )
        return result.scalars().all()

    async def search_technologies(self, query: str):
        result = await self.db.execute(
            select(Technology)
            .where(
                func.lower(Technology.name).contains(
                    query.lower()
                )
            )
            .order_by(Technology.name)
        )
        return result.scalars().all()

    async def get_technology_by_name(self, name: str):
        result = await self.db.execute(
            select(Technology).where(
                func.lower(Technology.name)
                == name.lower()
            )
        )
        return result.scalar_one_or_none()

    async def create_technology(self, name: str):
        technology = Technology(name=name)

        self.db.add(technology)

        await self.db.flush()
        await self.db.refresh(technology)

        return technology