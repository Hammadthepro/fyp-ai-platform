from sqlalchemy.ext.asyncio import AsyncSession

from app.master.repository import MasterRepository


class MasterService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = MasterRepository(db)

    # ---------- Helpers ----------

    @staticmethod
    def normalize_name(name: str) -> str:
        return " ".join(
            word.capitalize()
            for word in name.strip().split()
        )

    # ---------- Skills ----------

    async def get_skills(self):
        return await self.repo.get_all_skills()

    async def search_skills(self, query: str):
        return await self.repo.search_skills(query)

    async def create_skill(self, name: str):
        name = self.normalize_name(name)

        skill = await self.repo.get_skill_by_name(name)

        if skill:
            return skill

        skill = await self.repo.create_skill(name)

        await self.db.commit()

        return skill

    # ---------- Domains ----------

    async def get_domains(self):
        return await self.repo.get_all_domains()

    async def search_domains(self, query: str):
        return await self.repo.search_domains(query)

    async def create_domain(self, name: str):
        name = self.normalize_name(name)

        domain = await self.repo.get_domain_by_name(name)

        if domain:
            return domain

        domain = await self.repo.create_domain(name)

        await self.db.commit()

        return domain


        # ---------- Technologies ----------

    async def get_technologies(self):
        return await self.repo.get_all_technologies()

    async def search_technologies(self, query: str):
        return await self.repo.search_technologies(query)

    async def create_technology(self, name: str):
        name = self.normalize_name(name)

        technology = await self.repo.get_technology_by_name(name)

        if technology:
            return technology

        technology = await self.repo.create_technology(name)

        await self.db.commit()

        return technology