from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.tasks import TaskService

from fastapi import Depends

async def get_task_service(session: AsyncSession = Depends(get_db)):
    return TaskService(session)

