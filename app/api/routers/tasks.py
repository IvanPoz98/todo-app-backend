from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_task_service
from app.schemas.tasks import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.tasks import TaskNotFoundError, TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('', status_code=status.HTTP_200_OK, response_model=list[TaskSchema])
async def get_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return await task_service.list_tasks()

@router.post('', status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def create_task(payload: TaskCreateSchema, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return await task_service.create_task(payload)

@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def update_task(id: str, payload: TaskUpdateSchema, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    try:
        return await task_service.update_task(id, payload)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return await task_service.delete_task(id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')