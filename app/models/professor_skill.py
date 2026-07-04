from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class ProfessorSkill(BaseModel):
    __tablename__ = "professor_skills"

    professor_id: Mapped[UUID] = mapped_column(
        ForeignKey("professors.id", ondelete="CASCADE"),
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
    )

    professor: Mapped["Professor"] = relationship(
        "Professor",
        back_populates="skills",
    )

    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="professor_skills",
    )