from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    room_id: Mapped[str] = mapped_column(
        ForeignKey(
            "chat_rooms.id",
            ondelete="CASCADE",
        )
    )

    sender_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_ai: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    room = relationship(
        "ChatRoom",
        back_populates="messages",
    )

    sender = relationship(
        "User",
    )