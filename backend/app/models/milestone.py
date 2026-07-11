from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Milestone(BaseModel):
    __tablename__ = "milestones"

    group_id: Mapped[str] = mapped_column(
        ForeignKey("groups.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    group = relationship(
        "Group",
        back_populates="milestones",
    )

    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="milestone",
        cascade="all, delete-orphan",
    )