from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from tortoise import Tortoise
from config import settings
from modules.assets.router import router as asset_router
from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.organizations.router import router as organizations_router
from tortoise.contrib.fastapi import register_tortoise
from database import modules

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    summary=settings.PROJECT_SUMMARY,
)

Tortoise.init_models(modules, "models")

register_tortoise(
    app,
    db_url=settings.PSQL_CONNECT_STR,
    modules=modules,
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(asset_router)


@app.get("/")
async def main():
    return RedirectResponse(url="/docs")


@app.get("/ping")
async def ping() -> JSONResponse:
    return JSONResponse("PONG")
