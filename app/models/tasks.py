from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(String(255))
    completed: Mapped[bool] = mapped_column(default = False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    