from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel


class Group(BaseModel):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    leader_id = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    supervisor_id = mapped_column(
        ForeignKey(
            "professors.id"
        ),
        nullable=True,
    )

    supervisor = relationship(
        "Professor",
        back_populates="groups",
    )

    leader = relationship(
        "Student",
        foreign_keys=[leader_id],
        overlaps="led_groups",
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

    proposals = relationship(
        "Proposal",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    milestones = relationship(
        "Milestone",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    chat_room = relationship(
        "ChatRoom",
        back_populates="group",
        uselist=False,
        cascade="all, delete-orphan",
    )