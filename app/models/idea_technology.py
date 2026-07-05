from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class IdeaTechnology(BaseModel):
    __tablename__ = "idea_technologies"

    idea_id: Mapped[UUID] = mapped_column(
        ForeignKey("fyp_ideas.id", ondelete="CASCADE")
    )

    technology_id: Mapped[UUID] = mapped_column(
        ForeignKey("technologies.id", ondelete="CASCADE")
    )

    technology = relationship("Technology")