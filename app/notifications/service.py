from uuid import UUID

from fastapi import HTTPException

from app.models.notification import Notification
from app.notifications.repository import NotificationRepository


class NotificationService:

    def __init__(self, db):
        self.db = db
        self.repo = NotificationRepository(db)

    # =====================================================
    # CREATE
    # =====================================================

    async def create(
        self,
        user_id: UUID,
        title: str,
        message: str,
        type: str = "General",
    ):

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
        )

        await self.repo.create(notification)

        await self.db.commit()

        return notification

    # =====================================================
    # GET ALL
    # =====================================================

    async def get_all(
        self,
        current_user,
    ):

        return await self.repo.get_user_notifications(
            current_user.id
        )

    # =====================================================
    # GET UNREAD
    # =====================================================

    async def get_unread(
        self,
        current_user,
    ):

        return await self.repo.get_unread(
            current_user.id
        )

    # =====================================================
    # UNREAD COUNT
    # =====================================================

    async def unread_count(
        self,
        current_user,
    ):

        unread = await self.repo.get_unread(
            current_user.id
        )

        return {
            "unread": len(unread)
        }

    # =====================================================
    # MARK READ
    # =====================================================

    async def mark_read(
        self,
        current_user,
        notification_id: UUID,
    ):

        notification = await self.repo.get(
            notification_id
        )

        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found.",
            )

        if notification.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        notification.is_read = True

        await self.repo.update(notification)

        await self.db.commit()

        return notification

    # =====================================================
    # MARK ALL READ
    # =====================================================

    async def mark_all_read(
        self,
        current_user,
    ):

        await self.repo.mark_all_read(
            current_user.id
        )

        await self.db.commit()

        return {
            "message": "All notifications marked as read."
        }

    # =====================================================
    # DELETE
    # =====================================================

    async def delete(
        self,
        current_user,
        notification_id: UUID,
    ):

        notification = await self.repo.get(
            notification_id
        )

        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found.",
            )

        if notification.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        await self.repo.delete(notification)

        await self.db.commit()

        return {
            "message": "Notification deleted."
        }

    # =====================================================
    # DELETE ALL
    # =====================================================

    async def delete_all(
        self,
        current_user,
    ):

        await self.repo.delete_all(
            current_user.id
        )

        await self.db.commit()

        return {
            "message": "All notifications deleted."
        }