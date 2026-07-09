from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


class NotificationRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    async def create(
        self,
        notification: Notification,
    ):
        self.db.add(notification)

        await self.db.flush()
        await self.db.refresh(notification)

        return notification

    # =====================================================
    # GET ALL
    # =====================================================

    async def get_user_notifications(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Notification)
            .where(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
        )

        return result.scalars().all()

    # =====================================================
    # GET UNREAD
    # =====================================================

    async def get_unread(
        self,
        user_id: UUID,
    ):
        result = await self.db.execute(
            select(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
            .order_by(
                Notification.created_at.desc()
            )
        )

        return result.scalars().all()

    # =====================================================
    # GET SINGLE
    # =====================================================

    async def get(
        self,
        notification_id: UUID,
    ):
        result = await self.db.execute(
            select(Notification).where(
                Notification.id == notification_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update(
        self,
        notification: Notification,
    ):
        await self.db.flush()
        await self.db.refresh(notification)

        return notification

    # =====================================================
    # DELETE
    # =====================================================

    async def delete(
        self,
        notification: Notification,
    ):
        await self.db.delete(notification)

    # =====================================================
    # DELETE ALL
    # =====================================================

    async def delete_all(
        self,
        user_id: UUID,
    ):
        notifications = await self.get_user_notifications(
            user_id
        )

        for notification in notifications:
            await self.db.delete(notification)

    # =====================================================
    # MARK ALL READ
    # =====================================================

    async def mark_all_read(
        self,
        user_id: UUID,
    ):
        notifications = await self.get_unread(
            user_id
        )

        for notification in notifications:
            notification.is_read = True

        await self.db.flush()

        return notifications