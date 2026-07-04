from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class ProfessorDomain(BaseModel):
    __tablename__ = "professor_domains"

    professor_id: Mapped[UUID] = mapped_column(
        ForeignKey("professors.id", ondelete="CASCADE"),
    )

    domain_id: Mapped[UUID] = mapped_column(
        ForeignKey("domains.id", ondelete="CASCADE"),
    )

    professor: Mapped["Professor"] = relationship(
        "Professor",
        back_populates="domains",
    )

    domain: Mapped["Domain"] = relationship(
        "Domain",
        back_populates="professor_domains",
    )