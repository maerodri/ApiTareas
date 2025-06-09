
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from datetime import datetime




@pytest.mark.asyncio
async def test_create_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        nameList = "Tarea_"+datetime.now().strftime("%H%M/%S");
        response = await ac.post("/lists/", json={"name": nameList})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == nameList
    assert "id" in data


@pytest.mark.asyncio
async def test_create_list_missing_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/lists/", json={})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_list_empty_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/lists/", json={"name": 2232})
    assert res.status_code in [400, 422]

