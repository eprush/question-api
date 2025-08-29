"""
A module describing base model
"""
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    repr_cols_num = 1
    repr_cols = tuple()

    def __repr__(self):
        columns = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                columns.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {", ".join(columns)}>"
