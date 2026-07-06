from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel

class Group(BaseModel):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    leader_id = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )

    leader = relationship(
        "Student",
        foreign_keys=[leader_id],
    )

    members = relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    invitations = relationship(
        "GroupInvitation",
        back_populates="group",
        cascade="all, delete-orphan",
    )