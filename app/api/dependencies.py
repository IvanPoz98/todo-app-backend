from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.tasks import TaskService
from app.services.auth import AuthService

from fastapi import Depends

async def get_task_service(session: AsyncSession = Depends(get_db)):
    return TaskService(session)


async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session)