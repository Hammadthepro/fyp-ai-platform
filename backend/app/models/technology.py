from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base_model import BaseModel


class Technology(BaseModel):
    __tablename__ = "technologies"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )