from pydantic import BaseModel
from typing import Optional
from enum import Enum
from typing import Optional

class ListCreate(BaseModel):
    name: str

class ListOut(BaseModel):
    id: int
    name: str

class Config:
    orm_mode = True 

class ListUpdate(BaseModel):
    name: str

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.pending
    list_id: int
    assigned_user_id: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    list_id: int
    assigned_user_id: Optional[int]


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[TaskPriority]
    status: Optional[TaskStatus]
    list_id: Optional[int]
    assigned_user_id: Optional[int]

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class TaskListWithCompletion(BaseModel):
    tasks: list[TaskOut]
    completion: float

class UserOut(BaseModel):
    id: int
    username: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    hashed_password: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str]
    hashed_password: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
    
