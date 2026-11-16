from app.models.user import UserORM

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> UserORM | None:
        result = await self.db.scalars(
            select(UserORM).where(UserORM.email == email)
        )
        return result.first()

    async def create(self, email: str, hashed_password: str) -> UserORM:
        user = UserORM(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: str) -> UserORM | None:
        return await self.db.get(UserORM, user_id)
