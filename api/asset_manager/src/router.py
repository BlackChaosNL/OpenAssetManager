from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse


router = APIRouter(prefix="/api/v1")


@router.get("/")
async def main() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/ping")
async def ping() -> JSONResponse:
    return {"ping": "pong!"}
