import pytest # type: ignore
from httpx import AsyncClient


class TestRootRoute(object):
    async def test_read_docs_on_main_route(self, client: AsyncClient):
        response = await client.get("https://localhost/api/v1/")
        assert response.status_code == 307

    async def test_get_pong(self, client: AsyncClient):
        response = await client.get("https://localhost/api/v1/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}
