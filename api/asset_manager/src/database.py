from typing_extensions import Any
from tortoise import Tortoise
import os

db_url = os.getenv('PSQL_CONNECT_STR')
modules: dict[str, Any] = {'models': [
    '.models',
    '.modules.auth.models',
    '.modules.assets.models',
]}

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init_db():
    await Tortoise.init(
        db_url=db_url,
        modules=modules
    )

async def migrate_db():
    await init_db()

    # Generate the schema
    await Tortoise.generate_schemas(safe=True)
