from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.models import List, Task, User
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, delete, func
from app.domain.schemas import TaskStatus, TaskPriority
from passlib.context import CryptContext
from app.infrastructure import notifications

async def get_all_lists(db: AsyncSession):
    result = await db.execute(select(List))
    return result.scalars().all()

async def create_list(db: AsyncSession, name: str):
    new_list = List(name=name)
    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)
    return new_list

async def update_list(db: AsyncSession, list_id: int, name: str):
    result = await db.execute(select(List).where(List.id == list_id))
    list_obj = result.scalar_one_or_none()
    if not list_obj:
        raise NoResultFound
    list_obj.name = name
    await db.commit()
    await db.refresh(list_obj)
    return list_obj

async def delete_list(db: AsyncSession, list_id: int):
    result = await db.execute(select(List).where(List.id == list_id))
    list_obj = result.scalar_one_or_none()
    if not list_obj:
        raise NoResultFound
    await db.delete(list_obj)
    await db.commit()
    return {"message": f"Lista {list_id} eliminada"}

async def get_all_tasks(db: AsyncSession, status: TaskStatus = None, priority: TaskPriority = None):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    result = await db.execute(query)
    return result.scalars().all()

async def create_task(db: AsyncSession, task_data: dict):
    task = Task(**task_data)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    if task.assigned_user_id:
        result = await db.execute(select(User).where(User.id == task.assigned_user_id))
        user = result.scalar_one_or_none()
        if user:
            notifications.send_task_notification(user.username + "@gmail.com", task.title)


    return task

async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise NoResultFound
    return task

async def update_task(db: AsyncSession, task_id: int, updates: dict):
    task = await get_task_by_id(db, task_id)
    for key, value in updates.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int):
    task = await get_task_by_id(db, task_id)
    await db.delete(task)
    await db.commit()
    return {"message": f"Tarea {task_id} eliminada"}

async def get_tasks_by_list_with_stats(db: AsyncSession, list_id: int, status=None, priority=None):
    query = select(Task).where(Task.list_id == list_id)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)

    result = await db.execute(query)
    tasks = result.scalars().all()

    # Calcular porcentaje de completitud
    total = len(tasks)
    done = len([task for task in tasks if task.status == TaskStatus.done])
    completion = (done / total * 100) if total > 0 else 0

    return {
        "tasks": tasks,
        "completion": round(completion, 2)
    }

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, username: str, password: str):
    hashed = hash_password(password)
    user = User(username=username, hashed_password=hashed)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise NoResultFound
    return user

async def update_user(db: AsyncSession, user_id: int, updates: dict):
    user = await get_user_by_id(db, user_id)
    if "hashed_password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("hashed_password"))
    for key, value in updates.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
    return {"message": f"Usuario {user_id} eliminado"}
