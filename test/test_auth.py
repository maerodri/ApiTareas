import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/", json={"username": "loginuser", "password": "pass123"})
        res = await ac.post("/login", data={"username": "loginuser", "password": "pass123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_login_wrong_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/", json={"username": "wrongpass", "password": "abc"})
        res = await ac.post("/login", data={"username": "wrongpass", "password": "zzz"})
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_login_user_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/login", data={"username": "nouser", "password": "nada"})
    assert res.status_code == 404