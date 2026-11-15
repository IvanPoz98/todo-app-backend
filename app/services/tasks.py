from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import TaskORM
from app.schemas.tasks import TaskUpdateSchema
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreateSchema

class TaskNotFoundError(Exception):
    ...


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = TaskRepository(db)
    

    async def list_tasks(self) -> list[TaskORM]:
        return await self.repository.get_all()


    async def create_task(self, payload: TaskCreateSchema) -> TaskORM:
        new_task = await self.repository.create(
            task_title=payload.title, 
            task_description=payload.description
        )
        await self.db.commit()
        return new_task


    async def update_task(self, task_id: str, payload: TaskUpdateSchema) -> TaskORM:
        update_task = await self.repository.get_by_id(
            task_id=task_id
        )
        if not update_task:
            raise TaskNotFoundError()

        if payload.title is not None:
            update_task.title =  payload.title
        if payload.completed is not None:
            update_task.completed = payload.completed
        if payload.description is not None: 
            update_task.description = payload.description

        await self.db.commit()
        return update_task


    async def delete_task(self, task_id: str) -> None:
        del_task = await self.repository.get_by_id(task_id=task_id)
        if not del_task:
            raise TaskNotFoundError()

        await self.repository.delete(task=del_task)
        await self.db.commit()