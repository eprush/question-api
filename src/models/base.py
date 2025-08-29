"""
A module describing base model
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    repr_cols_num = 1
    repr_cols = tuple()

    def __repr__(self):
        columns = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                columns.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {", ".join(columns)}>"
