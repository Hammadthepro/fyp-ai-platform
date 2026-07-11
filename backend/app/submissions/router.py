from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.submissions.schemas import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionUpdate,
)
from app.submissions.service import SubmissionService

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "",
    response_model=SubmissionResponse,
)
async def submit_milestone(
    data: SubmissionCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)

    return await service.submit(
        current_user,
        data,
    )


@router.get(
    "/milestone/{milestone_id}",
    response_model=list[SubmissionResponse],
)
async def get_submissions(
    milestone_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)

    return await service.get_submissions(
        milestone_id,
    )


@router.patch(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
async def update_submission(
    submission_id: UUID,
    data: SubmissionUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = SubmissionService(db)

    return await service.update_submission(
        current_user,
        submission_id,
        data,
    )