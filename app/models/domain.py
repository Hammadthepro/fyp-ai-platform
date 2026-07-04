from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Domain(BaseModel):
    __tablename__ = "domains"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    student_domains: Mapped[list["StudentDomain"]] = relationship(
        "StudentDomain",
        back_populates="domain",
        cascade="all, delete-orphan",
    )

    professor_domains: Mapped[list["ProfessorDomain"]] = relationship(
        "ProfessorDomain",
        back_populates="domain",
        cascade="all, delete-orphan",
    )