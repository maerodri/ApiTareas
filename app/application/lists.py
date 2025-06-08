from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import SessionLocal
from app.infrastructure import repositories
from app.domain import schemas
from sqlalchemy.exc import NoResultFound
from app.domain.schemas import ListUpdate

router = APIRouter()

# Dependencia para obtener sesión de BD
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[schemas.ListOut])
async def read_lists(db: AsyncSession = Depends(get_db)):
    return await repositories.get_all_lists(db)

@router.post("/", response_model=schemas.ListOut)
async def create_list(list_in: schemas.ListCreate, db: AsyncSession = Depends(get_db)):
    return await repositories.create_list(db, list_in.name)

@router.put("/{list_id}", response_model=schemas.ListOut)
async def update_list(
    list_id: int, list_in: ListUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        return await repositories.update_list(db, list_id, list_in.name)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Lista no encontrada")

@router.delete("/{list_id}")
async def delete_list(list_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await repositories.delete_list(db, list_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
