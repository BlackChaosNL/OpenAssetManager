from fastapi import FastAPI
from starlette.responses import RedirectResponse
from src.config import settings
from src.modules.assets.router import router as asset_router
from tortoise.contrib.fastapi import register_tortoise
from src.database import db_url, modules

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    summary=settings.PROJECT_SUMMARY,
)

register_tortoise(
    app,
    db_url=db_url,
    modules=modules,
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(asset_router)


@app.get("/")
async def main():
    return RedirectResponse(url="/docs")
