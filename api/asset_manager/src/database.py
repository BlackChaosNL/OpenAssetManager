from typing_extensions import Any
from tortoise import Tortoise
from config import settings
from aerich import Command

modules: dict[str, Any] = {
    "models": [
        "modules.auth.models",
        "modules.users.models",
        "modules.organizations.models",
    ]
}

TORTOISE_ORM = {
    "connections": {
        "testing": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": "stoneedge.sqlite"
            }
        },
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.PSQL_HOSTNAME,
                "database": settings.PSQL_DB_NAME,
                "user": settings.PSQL_USERNAME,
                "password": settings.PSQL_PASSWORD,
                "port": settings.PSQL_PORT,
            },
        }
    },
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "testing" if settings.IS_TESTING else "default",
        },
    },
}


async def migrate_db():
    aerich = Command(tortoise_config=TORTOISE_ORM)
    await aerich.init()
    await aerich.upgrade(run_in_transaction=True)
    await Tortoise.init(config=TORTOISE_ORM)

async def end_connections_to_db():
    await Tortoise.close_connections()