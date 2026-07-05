from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class IdeaSkill(BaseModel):
    __tablename__ = "idea_skills"

    idea_id: Mapped[UUID] = mapped_column(
        ForeignKey("fyp_ideas.id", ondelete="CASCADE")
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE")
    )

    skill = relationship("Skill")