from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.ideas.repository import IdeaRepository
from app.ideas.schemas import IdeaCreate, IdeaUpdate
from app.models.fyp_idea import FYPIdea
from app.models.professor import Professor


class IdeaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = IdeaRepository(db)

    # ---------------------------------------
    # Helpers
    # ---------------------------------------

    async def _get_professor(
        self,
        user: User,
    ) -> Professor:

        professor = await self.repo.get_professor_by_user(
            user.id
        )

        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor profile not found.",
            )

        return professor

    async def _validate_domain(
        self,
        domain_id: UUID,
    ):
        domain = await self.repo.get_domain(domain_id)

        if not domain:
            raise HTTPException(
                status_code=404,
                detail="Domain not found.",
            )

    async def _validate_skills(
        self,
        ids: list[UUID],
    ):
        skills = await self.repo.get_skills(ids)

        if len(skills) != len(ids):
            raise HTTPException(
                status_code=404,
                detail="One or more skills do not exist.",
            )

    async def _validate_technologies(
        self,
        ids: list[UUID],
    ):
        techs = await self.repo.get_technologies(ids)

        if len(techs) != len(ids):
            raise HTTPException(
                status_code=404,
                detail="One or more technologies do not exist.",
            )

    # ---------------------------------------
    # Create
    # ---------------------------------------

    async def create_idea(
        self,
        user: User,
        data: IdeaCreate,
    ):

        professor = await self._get_professor(user)

        await self._validate_domain(data.domain_id)

        await self._validate_skills(
            data.skill_ids,
        )

        await self._validate_technologies(
            data.technology_ids,
        )

        idea = FYPIdea(
            professor_id=professor.id,
            title=data.title,
            description=data.description,
            domain_id=data.domain_id,
            difficulty=data.difficulty,
            max_students=data.max_students,
        )

        await self.repo.create(idea)

        await self.repo.replace_skills(
            idea.id,
            data.skill_ids,
        )

        await self.repo.replace_technologies(
            idea.id,
            data.technology_ids,
        )

        await self.db.commit()

        return await self.repo.get_by_id(
            idea.id,
        )

    # ---------------------------------------
    # My Ideas
    # ---------------------------------------

    async def my_ideas(
        self,
        user: User,
    ):

        professor = await self._get_professor(user)

        return await self.repo.get_professor_ideas(
            professor.id,
        )

    # ---------------------------------------
    # Single Idea
    # ---------------------------------------

    async def get_idea(
        self,
        idea_id: UUID,
    ):

        idea = await self.repo.get_by_id(
            idea_id,
        )

        if not idea:
            raise HTTPException(
                status_code=404,
                detail="Idea not found.",
            )

        return idea

    # ---------------------------------------
    # Update
    # ---------------------------------------

    async def update_idea(
        self,
        user: User,
        idea_id: UUID,
        data: IdeaUpdate,
    ):

        professor = await self._get_professor(user)

        idea = await self.repo.get_professor_idea(
            professor.id,
            idea_id,
        )

        if not idea:
            raise HTTPException(
                status_code=404,
                detail="Idea not found.",
            )

        values = data.model_dump(
            exclude_unset=True,
        )

        if "domain_id" in values:
            await self._validate_domain(
                values["domain_id"]
            )

        if "skill_ids" in values:
            await self._validate_skills(
                values["skill_ids"]
            )

        if "technology_ids" in values:
            await self._validate_technologies(
                values["technology_ids"]
            )

        for field in [
            "title",
            "description",
            "domain_id",
            "difficulty",
            "max_students",
            "is_active",
        ]:
            if field in values:
                setattr(
                    idea,
                    field,
                    values[field],
                )

        if "skill_ids" in values:
            await self.repo.replace_skills(
                idea.id,
                values["skill_ids"],
            )

        if "technology_ids" in values:
            await self.repo.replace_technologies(
                idea.id,
                values["technology_ids"],
            )

        await self.db.commit()

        return await self.repo.get_by_id(
            idea.id,
        )

    # ---------------------------------------
    # Delete
    # ---------------------------------------

    async def delete_idea(
        self,
        user: User,
        idea_id: UUID,
    ):

        professor = await self._get_professor(
            user,
        )

        idea = await self.repo.get_professor_idea(
            professor.id,
            idea_id,
        )

        if not idea:
            raise HTTPException(
                status_code=404,
                detail="Idea not found.",
            )

        await self.repo.delete(
            idea,
        )

        await self.db.commit()

        return {
            "message": "Idea deleted successfully."
        }


    async def list_ideas(
        self,
        keyword: str |None=None,
        domain_id: UUID |None=None,
        difficulty: str |None=None,
        technology_id: UUID |None=None,
        skill_id: UUID |None=None,
        professor: str |None=None,
        newest: bool=True,
    ):
        return await self.repo.list_ideas(
            keyword,
            domain_id,
            difficulty,
            technology_id,
            skill_id,
            professor,
            newest,
        )