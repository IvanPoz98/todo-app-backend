from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.security import decode_access_token
from app.db.session import get_db
from app.services.tasks import TaskService
from app.models.user import UserORM
from app.repositories.users import UserRepository
from app.services.auth import AuthService

security_schema = HTTPBearer()


async def get_task_service(session: AsyncSession = Depends(get_db)):
    return TaskService(session)


async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_schema),
    session: AsyncSession = Depends(get_db)
    ) -> UserORM:
    token = credentials.credentials

    try:
        user_id = decode_access_token(token)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found",
        )

    return user
