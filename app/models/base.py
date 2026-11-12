from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default = lambda: str(uuid4()))

