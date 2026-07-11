from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class FYPIdea(BaseModel):
    __tablename__ = "fyp_ideas"

    professor_id: Mapped[UUID] = mapped_column(
        ForeignKey("professors.id", ondelete="CASCADE"),
        nullable=False,
    )

    domain_id: Mapped[UUID] = mapped_column(
        ForeignKey("domains.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        default="Intermediate",
    )

    max_students: Mapped[int] = mapped_column(
        Integer,
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

    domain = relationship("Domain")

    technologies = relationship(
        "IdeaTechnology",
        backref="idea",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    skills = relationship(
        "IdeaSkill",
        backref="idea",
        cascade="all, delete-orphan",
        lazy="selectin",
    )