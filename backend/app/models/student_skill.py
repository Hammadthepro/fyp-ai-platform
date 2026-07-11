from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class StudentSkill(BaseModel):
    __tablename__ = "student_skills"

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="skills",
    )

    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="student_skills",
    )