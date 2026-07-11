from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.chat_message import ChatMessage
from app.models.chat_room import ChatRoom
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.student import Student

class ChatRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ==========================================
    # ROOM
    # ==========================================

    async def get_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(Group)
            .options(
                selectinload(Group.supervisor)
            )
            .where(
                Group.id == group_id
            )
        )

        return result.scalar_one_or_none()

    async def get_room(
        self,
        room_id: UUID,
    ):
        result = await self.db.execute(
            select(ChatRoom).where(
                ChatRoom.id == room_id
            )
        )

        return result.scalar_one_or_none()

    async def get_room_by_group(
        self,
        group_id: UUID,
    ):
        result = await self.db.execute(
            select(ChatRoom).where(
                ChatRoom.group_id == group_id
            )
        )

        return result.scalar_one_or_none()

    async def create_room(
        self,
        room: ChatRoom,
    ):
        self.db.add(room)

        await self.db.flush()
        await self.db.refresh(room)

        return room

    # ==========================================
    # MESSAGE
    # ==========================================

    async def create_message(
        self,
        message: ChatMessage,
    ):
        self.db.add(message)

        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def get_message(
        self,
        message_id: UUID,
    ):
        result = await self.db.execute(
            select(ChatMessage).where(
                ChatMessage.id == message_id
            )
        )

        return result.scalar_one_or_none()

    async def get_messages(
        self,
        room_id: UUID,
    ):
        result = await self.db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.room_id == room_id
            )
            .order_by(
                ChatMessage.created_at
            )
        )

        return result.scalars().all()

    async def delete_message(
        self,
        message: ChatMessage,
    ):
        await self.db.delete(message)


        # ==========================================
    # PERMISSIONS
    # ==========================================

    async def is_group_member(
        self,
        group_id: UUID,
        user_id: UUID,
    ):
        group = await self.get_group(
            group_id
        )

        if not group:
            return False

        # Supervisor can access the chat
        if (
            group.supervisor
            and group.supervisor.user_id == user_id
        ):
            return True

        result = await self.db.execute(
            select(GroupMember)
            .join(
                Student,
                Student.id == GroupMember.student_id,
            )
            .where(
                GroupMember.group_id == group_id,
                Student.user_id == user_id,
            )
        )

        return (
            result.scalar_one_or_none()
            is not None
        )