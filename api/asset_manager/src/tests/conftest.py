import asyncio, httpx, pytest
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from asgi_lifespan import LifespanManager

from tests.fixtures.account import *

try:
    from main import app
except ImportError:
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    from main import app

ClientManagerType = AsyncGenerator[httpx.AsyncClient, None]


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@asynccontextmanager
async def client_manager(app, base_url="https://localhost", **kw) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url=base_url, **kw
        ) as c:
            yield c


@pytest.fixture(scope="module")
async def client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c
