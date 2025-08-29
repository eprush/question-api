"""
A module describing question model
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Question(BaseModel):
    """Question model."""

    __tablename__ = "questions"

    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

from src.models.answer import Answer  # noqa: E402
