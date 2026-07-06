from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Student(BaseModel):
    __tablename__ = "students"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    registration_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    semester: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    skills: Mapped[list["StudentSkill"]] = relationship(
        "StudentSkill",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    domains: Mapped[list["StudentDomain"]] = relationship(
        "StudentDomain",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    github: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    linkedin: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    portfolio: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="student",
    )

    groups = relationship(
        "GroupMember",
        back_populates="student",
    )

    led_groups = relationship(
        "Group",
        foreign_keys="Group.leader_id",
    )