from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel

class CalendarEvent(BaseModel):
    __tablename__ = "calendar_events"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        default="General",
    )

    start_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_all_day: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_by: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
    )

    group_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("groups.id"),
        nullable=True,
    )

    creator = relationship(
        "User",
        lazy="selectin",
    )

    group = relationship(
        "Group",
        lazy="selectin",
    )