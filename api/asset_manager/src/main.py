from fastapi import FastAPI
from config import settings
from database import end_connections_to_db, migrate_db
from responses import msgspec_jsonresponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from router import router as root_router
from modules.assets.router import router as asset_router
from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.organizations.router import router as organizations_router
from modules.invitations.router import router as invitations_router

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

@asynccontextmanager
async def lifespan(_: FastAPI):
    await migrate_db()
    yield
    await end_connections_to_db()


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    summary=settings.PROJECT_SUMMARY,
    default_response_class=msgspec_jsonresponse,
)

if settings.USE_HTTPS_ONLY:
    app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        settings.PROJECT_PUBLIC_URL,
    ],
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(asset_router)
app.include_router(invitations_router)
