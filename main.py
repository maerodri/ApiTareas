from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.application import lists, tasks, users


app = FastAPI(title="Prueba Técnica para Backend Developer")

app.version = "1.0.0"


# Crear las tablas al iniciar la app
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(lists.router, prefix="/lists", tags=["Lists"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(users.router, prefix="/users", tags=["Users"])
