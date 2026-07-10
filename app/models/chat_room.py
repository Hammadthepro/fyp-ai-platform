from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class ChatRoom(BaseModel):
    __tablename__ = "chat_rooms"

    group_id: Mapped[str] = mapped_column(
        ForeignKey(
            "groups.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    group = relationship(
        "Group",
        back_populates="chat_room",
    )

    messages = relationship(
        "ChatMessage",
        back_populates="room",
        cascade="all, delete-orphan",
    )