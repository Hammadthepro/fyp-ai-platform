from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from app.database.base_model import BaseModel

class GroupMember(BaseModel):
    __tablename__ = "group_members"

    group_id = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
    )

    student_id = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    group = relationship(
        "Group",
        back_populates="members",
    )

    student = relationship(
        "Student",
    )