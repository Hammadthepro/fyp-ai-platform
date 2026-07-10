from app.models.chat_message import ChatMessage


class ChatWebSocketService:

    def __init__(self, db):
        self.db = db

    async def save_message(
        self,
        room_id,
        sender_id,
        message,
    ):
        chat = ChatMessage(
            room_id=room_id,
            sender_id=sender_id,
            message=message,
        )

        self.db.add(chat)

        await self.db.commit()
        await self.db.refresh(chat)

        return chat