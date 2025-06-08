from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import SessionLocal
from app.domain import schemas
from app.infrastructure import repositories
from typing import Optional
from sqlalchemy.exc import NoResultFound
from app.domain.schemas import UserUpdate, LoginRequest, Token
from app.infrastructure.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from passlib.context import CryptContext
from app.infrastructure.models import User

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[schemas.UserOut])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await repositories.get_all_users(db)

@router.post("/", response_model=schemas.UserOut)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await repositories.create_user(db, user_in.username, user_in.hashed_password)

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await repositories.update_user(db, user_id, user_in.dict(exclude_unset=True))
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await repositories.delete_user(db, user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}