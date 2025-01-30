from typing import AsyncGenerator, Optional, Self
import httpx
from tortoise import Tortoise
import pytest  # type: ignore
from database import modules
from config import settings

from asgi_lifespan import LifespanManager # type: ignore

try:
    from main import app
except ImportError:
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    from main import app

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.PSQL_HOSTNAME,
                "database": settings.PSQL_TEST_DB_NAME,
                "user": settings.PSQL_USERNAME,
                "password": settings.PSQL_PASSWORD,
                "port": settings.PSQL_PORT,
            },
        }
    },
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default",
        },
    },
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


class TestClient(httpx.AsyncClient):
    def __init__(self, app, base_url="http://localhost", mount_lifespan=True, **kw) -> None:
        self.mount_lifespan = mount_lifespan
        self._manager: Optional[LifespanManager] = None
        super().__init__(transport=httpx.ASGITransport(app), base_url=base_url, **kw)

    async def __aenter__(self) -> Self:
        if self.mount_lifespan:
            app = self._transport.app  # type:ignore
            self._manager = await LifespanManager(app).__aenter__()
            self._transport = httpx.ASGITransport(app=self._manager.app)
        return await super().__aenter__()

    async def __aexit__(self, *args, **kw):
        await super().__aexit__(*args, **kw)
        if self._manager is not None:
            await self._manager.__aexit__(*args, **kw)

async def init_db(create_db: bool = True, schemas: bool = True) -> None:
    """Initial database connection"""
    await Tortoise.init(
        config=TORTOISE_ORM, timezone="Europe/Helsinki"
    )
    if create_db:
        print(f"Database created!")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")

@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init_db()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as c:
        yield c