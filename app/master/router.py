from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.master.schemas import (
    DomainCreate,
    DomainResponse,
    SkillCreate,
    SkillResponse,
    TechnologyCreate,
    TechnologyResponse,
)
from app.master.service import MasterService

router = APIRouter(
    prefix="/master",
    tags=["Master"],
)


# ---------- Skills ----------

@router.get(
    "/skills",
    response_model=list[SkillResponse],
)
async def get_skills(
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.get_skills()


@router.post(
    "/skills",
    response_model=SkillResponse,
)
async def create_skill(
    data: SkillCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.create_skill(data.name)


@router.get(
    "/skills/search",
    response_model=list[SkillResponse],
)
async def search_skills(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.search_skills(q)


# ---------- Domains ----------

@router.get(
    "/domains",
    response_model=list[DomainResponse],
)
async def get_domains(
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.get_domains()


@router.post(
    "/domains",
    response_model=DomainResponse,
)
async def create_domain(
    data: DomainCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.create_domain(data.name)


@router.get(
    "/domains/search",
    response_model=list[DomainResponse],
)
async def search_domains(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.search_domains(q)


# ---------- Technologies ----------

@router.get(
    "/technologies",
    response_model=list[TechnologyResponse],
)
async def get_technologies(
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.get_technologies()


@router.post(
    "/technologies",
    response_model=TechnologyResponse,
)
async def create_technology(
    data: TechnologyCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.create_technology(data.name)


@router.get(
    "/technologies/search",
    response_model=list[TechnologyResponse],
)
async def search_technologies(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    service = MasterService(db)
    return await service.search_technologies(q)