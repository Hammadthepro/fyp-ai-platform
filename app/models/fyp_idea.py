from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class FYPIdea(BaseModel):
    __tablename__ = "fyp_ideas"

    professor_id: Mapped[UUID] = mapped_column(
        ForeignKey("professors.id", ondelete="CASCADE"),
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    technologies: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    max_students: Mapped[int] = mapped_column(
        default=3,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    professor = relationship(
        "Professor",
        back_populates="ideas",
    )