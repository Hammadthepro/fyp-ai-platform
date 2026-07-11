from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class StudentDomain(BaseModel):
    __tablename__ = "student_domains"

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
    )

    domain_id: Mapped[UUID] = mapped_column(
        ForeignKey("domains.id", ondelete="CASCADE"),
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="domains",
    )

    domain: Mapped["Domain"] = relationship(
        "Domain",
        back_populates="student_domains",
    )