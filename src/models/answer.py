"""
A module describing answer model
"""

from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Answer(BaseModel):
    """Answer model."""

    __tablename__ = "answers"

    question_id: Mapped[id] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    repr_cols_num = 3

from src.models.question import Question # noqa: E402
