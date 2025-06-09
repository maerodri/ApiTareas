from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import SessionLocal
from app.domain import schemas
from app.infrastructure import repositories
from typing import Optional
from app.domain.schemas import TaskUpdate, TaskStatusUpdate, TaskStatus, TaskPriority
from sqlalchemy.exc import NoResultFound

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/", response_model=list[schemas.TaskOut])
async def read_tasks(
    status: Optional[schemas.TaskStatus] = Query(None),
    priority: Optional[schemas.TaskPriority] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.get_all_tasks(db, status, priority)


@router.post("/", response_model=schemas.TaskOut)
async def create_task(task_in: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await repositories.create_task(db, task_in.dict())


@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int, task_in: TaskUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        return await repositories.update_task(
            db, task_id, task_in.dict(exclude_unset=True)
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.patch("/{task_id}/status", response_model=schemas.TaskOut)
async def change_task_status(
    task_id: int, status_in: TaskStatusUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        return await repositories.update_task(db, task_id, {"status": status_in.status})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await repositories.delete_task(db, task_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.get("/list/{list_id}", response_model=schemas.TaskListWithCompletion)
async def get_tasks_by_list(
    list_id: int,
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.get_tasks_by_list_with_stats(
        db, list_id, status, priority
    )
