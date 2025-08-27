"""
A module describing answer model
"""


import uuid
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel

class Answer(BaseModel):
    """Answer model."""

    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[id] = mapped_column(ForeignKey("question.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True)
    text: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"Answer to question {self.question_id}, number {self.id}, was created on {self.created_at.date()}."
