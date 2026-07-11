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


class Submission(BaseModel):
    __tablename__ = "submissions"

    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id"),
        nullable=False,
    )

    submitted_by: Mapped[str] = mapped_column(
        ForeignKey("students.id"),
        nullable=False,
    )

    github_link: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    drive_link: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    marks: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Submitted",
    )

    milestone = relationship(
        "Milestone",
        back_populates="submissions",
    )

    student = relationship(
        "Student",
        back_populates="submissions",
    )