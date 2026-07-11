from uuid import UUID

from fastapi import HTTPException

from app.chat.repository import ChatRepository
from app.models.chat_message import ChatMessage
from app.models.chat_room import ChatRoom


class ChatService:

    def __init__(self, db):
        self.db = db
        self.repo = ChatRepository(db)

    # ==========================================
    # CREATE ROOM
    # ==========================================

    async def create_room(
        self,
        data,
    ):
        group = await self.repo.get_group(
            data.group_id
        )

        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found.",
            )

        existing = await self.repo.get_room_by_group(
            data.group_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Chat room already exists.",
            )

        room = ChatRoom(
            group_id=data.group_id,
            name=data.name,
        )

        await self.repo.create_room(room)

        await self.db.commit()
        await self.db.refresh(room)

        return room

        # ==========================================
    # SEND MESSAGE
    # ==========================================

    async def send_message(
        self,
        current_user,
        data,
    ):
        room = await self.repo.get_room(
            data.room_id
        )

        if not room:
            raise HTTPException(
                status_code=404,
                detail="Chat room not found.",
            )

        allowed = await self.repo.is_group_member(
            room.group_id,
            current_user.id,
        )

        role = str(current_user.role).lower()

        if not allowed and "admin" not in role:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this chat.",
            )

        message = ChatMessage(
            room_id=data.room_id,
            sender_id=current_user.id,
            message=data.message,
        )

        await self.repo.create_message(
            message
        )

        await self.db.commit()
        await self.db.refresh(message)

        return message
    # ==========================================
    # GET MESSAGES
    # ==========================================

    async def get_messages(
        self,
        current_user,
        room_id: UUID,
    ):
        room = await self.repo.get_room(
            room_id
        )

        if not room:
            raise HTTPException(
                status_code=404,
                detail="Chat room not found.",
            )

        allowed = await self.repo.is_group_member(
            room.group_id,
            current_user.id,
        )

        role = str(current_user.role).lower()

        if not allowed and "admin" not in role:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to view this chat.",
            )

        return await self.repo.get_messages(
            room_id
        )
    
    
    # ==========================================
    # UPDATE MESSAGE
    # ==========================================

    async def update_message(
        self,
        current_user,
        message_id: UUID,
        data,
    ):
        message = await self.repo.get_message(
            message_id
        )

        if not message:
            raise HTTPException(
                status_code=404,
                detail="Message not found.",
            )

        if message.sender_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only edit your own messages.",
            )

        message.message = data.message

        await self.db.commit()
        await self.db.refresh(message)

        return message

    # ==========================================
    # DELETE MESSAGE
    # ==========================================

    async def delete_message(
        self,
        current_user,
        message_id: UUID,
    ):
        message = await self.repo.get_message(
            message_id
        )

        if not message:
            raise HTTPException(
                status_code=404,
                detail="Message not found.",
            )

        role = str(current_user.role).lower()

        if (
            message.sender_id != current_user.id
            and "admin" not in role
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        await self.repo.delete_message(
            message
        )

        await self.db.commit()

        return {
            "message": "Message deleted successfully."
        }