from typing_extensions import Any
from tortoise import Tortoise
from config import settings

modules: dict[str, Any] = {
    "models": [
        "modules.assets.models",
        "modules.auth.models",
        "modules.users.models",
        "modules.organizations.models",
    ]
}

TORTOISE_ORM = {
    "connections": {"default": settings.PSQL_CONNECT_STR},
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)


async def migrate_db():
    await init_db()
    await Tortoise.generate_schemas(safe=True)
