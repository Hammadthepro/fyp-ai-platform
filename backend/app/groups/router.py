from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db

from app.groups.schemas import (
    GroupCreate,
    GroupInviteRequest,
    GroupResponse,
    InvitationAction,
    InvitationResponse,
)
from app.groups.service import GroupService

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)


@router.post(
    "",
    response_model=GroupResponse,
)
async def create_group(
    data: GroupCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GroupService(db)

    return await service.create_group(
        current_user,
        data,
    )


@router.post(
    "/{group_id}/invite",
    response_model=InvitationResponse,
)
async def invite_student(
    group_id: UUID,
    data: GroupInviteRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GroupService(db)

    return await service.invite_student(
        current_user,
        group_id,
        data.student_id,
    )


@router.post(
    "/invitations/{invitation_id}",
    response_model=InvitationResponse,
)
async def respond_to_invitation(
    invitation_id: UUID,
    data: InvitationAction,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GroupService(db)

    return await service.respond_to_invitation(
        current_user,
        invitation_id,
        data.action,
    )