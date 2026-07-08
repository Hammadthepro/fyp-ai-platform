from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.milestones.schemas import (
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneResponse,
)
from app.milestones.service import MilestoneService

router = APIRouter(
    prefix="/milestones",
    tags=["Milestones"],
)


@router.post(
    "/group/{group_id}",
    response_model=MilestoneResponse,
)
async def create_milestone(
    group_id: UUID,
    data: MilestoneCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MilestoneService(db)

    return await service.create_milestone(
        current_user,
        group_id,
        data,
    )


@router.get(
    "/group/{group_id}",
    response_model=list[MilestoneResponse],
)
async def get_group_milestones(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = MilestoneService(db)

    return await service.get_group_milestones(
        group_id,
    )


@router.put(
    "/{milestone_id}",
    response_model=MilestoneResponse,
)
async def update_milestone(
    milestone_id: UUID,
    data: MilestoneUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = MilestoneService(db)

    return await service.update_milestone(
        milestone_id,
        data,
    )


@router.delete(
    "/{milestone_id}",
)
async def delete_milestone(
    milestone_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = MilestoneService(db)

    return await service.delete_milestone(
        milestone_id,
    )