"""
A module describing question model
"""

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class Question(BaseModel):
    """Question model."""

    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
