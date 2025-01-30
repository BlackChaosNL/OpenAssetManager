from fastapi import FastAPI
from tortoise import run_async
from config import settings
from database import migrate_db
from responses import msgspec_jsonresponse

from router import router as root_router
from modules.assets.router import router as asset_router
from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.organizations.router import router as organizations_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    summary=settings.PROJECT_SUMMARY,
    default_response_class=msgspec_jsonresponse
)

run_async(migrate_db())

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(asset_router)
