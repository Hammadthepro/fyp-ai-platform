from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Query
from app.core.dependencies import get_current_user
from app.models.user import User
from app.database.database import get_db
from app.ideas.schemas import (
    IdeaCreate,
    IdeaResponse,
    IdeaUpdate,
)
from app.ideas.service import IdeaService

router = APIRouter(
    prefix="/ideas",
    tags=["Ideas"],
)


@router.post(
    "",
    response_model=IdeaResponse,
)
async def create_idea(
    data: IdeaCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.create_idea(
        current_user,
        data,
    )

@router.get(
    "",
    response_model=list[IdeaResponse],
)
async def list_ideas(
    keyword: str | None = None,
    domain_id: UUID | None = None,
    difficulty: str | None = None,
    technology_id: UUID | None = None,
    skill_id: UUID | None = None,
    professor: str | None = None,
    newest: bool = True,
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.list_ideas(
        keyword,
        domain_id,
        difficulty,
        technology_id,
        skill_id,
        professor,
        newest,
    )
       

@router.get(
    "/me",
    response_model=list[IdeaResponse],
)
async def my_ideas(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.my_ideas(
        current_user,
    )


@router.get(
    "/{idea_id}",
    response_model=IdeaResponse,
)
async def get_idea(
    idea_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.get_idea(
        idea_id,
    )


@router.put(
    "/{idea_id}",
    response_model=IdeaResponse,
)
async def update_idea(
    idea_id: UUID,
    data: IdeaUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.update_idea(
        current_user,
        idea_id,
        data,
    )


@router.delete(
    "/{idea_id}",
)
async def delete_idea(
    idea_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IdeaService(db)

    return await service.delete_idea(
        current_user,
        idea_id,
    )