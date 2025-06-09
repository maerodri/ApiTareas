import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_user_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/users/", json={"username": "manuel", "password": "123456"})
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "manuel"

@pytest.mark.asyncio
async def test_create_user_missing_fields():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/users/", json={})
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_create_user_duplicate_username():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/", json={"username": "duplicado", "password": "123"})
        res = await ac.post("/users/", json={"username": "duplicado", "password": "123"})
    assert res.status_code in [400, 409, 422]