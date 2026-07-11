from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from app.database.base_model import BaseModel

class GroupInvitation(BaseModel):
    __tablename__ = "group_invitations"

    group_id = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
    )

    student_id = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )

    status = mapped_column(
        String(20),
        default="Pending",
    )

    group = relationship(
        "Group",
        back_populates="invitations",
    )

    student = relationship(
        "Student",
    )