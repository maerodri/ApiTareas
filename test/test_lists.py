
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/lists/", json={"name": "Lista de prueba 4"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lista de prueba 4"
    assert "id" in data

