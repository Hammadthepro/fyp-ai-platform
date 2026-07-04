from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Professor(BaseModel):
    __tablename__ = "professors"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    employee_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    office: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    research_interests: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    max_groups: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    available_slots: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    user = relationship(
        "User",
        back_populates="professor",
    )

    skills: Mapped[list["ProfessorSkill"]] = relationship(
        "ProfessorSkill",
        back_populates="professor",
        cascade="all, delete-orphan",
    )

    domains: Mapped[list["ProfessorDomain"]] = relationship(
        "ProfessorDomain",
        back_populates="professor",
        cascade="all, delete-orphan",
    )

