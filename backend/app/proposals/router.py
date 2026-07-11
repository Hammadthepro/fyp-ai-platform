from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db

from app.proposals.schemas import (
    ProposalCreate,
    ProposalResponse,
    ProposalReview,
)
from app.proposals.service import ProposalService

router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
)


@router.post(
    "/groups/{group_id}",
    response_model=ProposalResponse,
)
async def create_proposal(
    group_id: UUID,
    data: ProposalCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProposalService(db)

    return await service.create_proposal(
        current_user,
        group_id,
        data,
    )


@router.get(
    "/pending",
    response_model=list[ProposalResponse],
)
async def get_pending_proposals(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProposalService(db)

    return await service.get_pending_proposals(
        current_user,
    )


@router.post(
    "/{proposal_id}/approve",
    response_model=ProposalResponse,
)
async def approve_proposal(
    proposal_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProposalService(db)

    return await service.approve_proposal(
        current_user,
        proposal_id,
    )


@router.post(
    "/{proposal_id}/reject",
    response_model=ProposalResponse,
)
async def reject_proposal(
    proposal_id: UUID,
    data: ProposalReview,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProposalService(db)

    return await service.reject_proposal(
        current_user,
        proposal_id,
        data.feedback,
    )