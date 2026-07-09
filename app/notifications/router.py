from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.notifications.service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =====================================================
# GET ALL
# =====================================================

@router.get("/")
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.get_all(
        current_user
    )


# =====================================================
# GET UNREAD
# =====================================================

@router.get("/unread")
async def unread_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.get_unread(
        current_user
    )


# =====================================================
# UNREAD COUNT
# =====================================================

@router.get("/count")
async def unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.unread_count(
        current_user
    )


# =====================================================
# MARK AS READ
# =====================================================

@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.mark_read(
        current_user,
        notification_id,
    )


# =====================================================
# MARK ALL AS READ
# =====================================================

@router.patch("/read-all")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.mark_all_read(
        current_user
    )


# =====================================================
# DELETE
# =====================================================

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.delete(
        current_user,
        notification_id,
    )


# =====================================================
# DELETE ALL
# =====================================================

@router.delete("/")
async def delete_all_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = NotificationService(db)

    return await service.delete_all(
        current_user
    )