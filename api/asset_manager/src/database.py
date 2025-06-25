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

TEST_TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:"
    },
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default",
        },
    },
}

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.PSQL_HOSTNAME,
                "database": settings.PSQL_DB_NAME,
                "user": settings.PSQL_USERNAME,
                "password": settings.PSQL_PASSWORD,
                "port": settings.PSQL_PORT,
            },
        },
    },
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default",
        },
    },
}


async def migrate_db(tortoise_config=TORTOISE_ORM):
    if settings.IS_TESTING:
        tortoise_config=TEST_TORTOISE_ORM
    aerich = Command(tortoise_config)
    await aerich.init()
    await aerich.upgrade()
    await Tortoise.init(tortoise_config)
    await Tortoise.generate_schemas(safe=True)


async def end_connections_to_db():
    await Tortoise.close_connections()
