from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base_model import BaseModel


class Proposal(BaseModel):
    __tablename__ = "proposals"

    group_id: Mapped[str] = mapped_column(
        ForeignKey("groups.id"),
        nullable=False,
    )

    professor_id: Mapped[str] = mapped_column(
        ForeignKey("professors.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
    )

    abstract: Mapped[str] = mapped_column(
        Text,
    )

    objectives: Mapped[str] = mapped_column(
        Text,
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
        back_populates="proposals",
    )

    professor = relationship(
        "Professor",
        back_populates="proposals",
    )