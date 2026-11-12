from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.tasks import TaskORM
from app.schemas.tasks import TaskUpdateSchema
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreateSchema

class TaskNotFoundError(Exception):
    ...


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = TaskRepository(session)
    
    async def list_tasks(self) -> list[TaskORM]:
        return await self.repository.get_all()

    async def create_task(self, data: TaskCreateSchema) -> TaskORM:
        new_task = await self.repository.create(task_title=data.title)
        await self.session.commit()
        return new_task

    async def update_task(self, task_id: str, data: TaskUpdateSchema) -> TaskORM:
        update_task = await self.repository.get_by_id(task_id=task_id)
        if not update_task:
            raise TaskNotFoundError()

        if data.title is not None:
            update_task.title =  data.title
        if data.completed is not None:
            update_task.completed = data.completed

        await self.session.commit()
        return update_task

    async def delete_task(self, task_id: str) -> None:
        del_task = await self.repository.get_by_id(task_id=task_id)
        if not del_task:
            raise TaskNotFoundError()

        await self.repository.delete(task=del_task)
        await self.session.commit()