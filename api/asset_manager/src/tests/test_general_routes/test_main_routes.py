import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_read_main(client: AsyncClient):
    response = await client.get("http://localhost:8000/api/v1/")
    assert response.status_code == 307


@pytest.mark.anyio
async def test_get_pong(client: AsyncClient):
    response = await client.get("http://localhost:8000/api/v1/ping")
    assert response.status_code == 200
    assert response.text == '"PONG"'
