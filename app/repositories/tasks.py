from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tasks import TaskORM
from sqlalchemy import select


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    

    async def get_all(self, user_id: str) -> list[TaskORM]:
        result = await self.db.scalars(select(TaskORM).where(TaskORM.user_id == user_id))
        return list(result.all())


    async def get_by_id(self, task_id: str) -> TaskORM | None:
        return await self.db.get(TaskORM, task_id)


    async def create(self, task_title: str, user_id: str, task_description: str | None = None) -> TaskORM:
        new_task = TaskORM(title=task_title, description=task_description, user_id=user_id)
        self.db.add(new_task)
        await self.db.flush()
        return new_task


    async def delete(self, task: TaskORM) -> None:
        await self.db.delete(task)
