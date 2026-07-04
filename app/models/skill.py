from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Skill(BaseModel):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    student_skills: Mapped[list["StudentSkill"]] = relationship(
        "StudentSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    professor_skills: Mapped[list["ProfessorSkill"]] = relationship(
        "ProfessorSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )