import os

from fastapi.security import OAuth2PasswordBearer

from fastapi.routing import APIRouter
from src.modules.auth.schemas import UserModel
from src.models import User
from fastapi import HTTPException
from src.config import settings

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

error: str = "E-Mail Address or password is incorrect"

@router.post("/")
async def login(email: str, password: str):
    user: User = await User.get_or_none(email=email)
    if user is None:
        HTTPException(status_code=401, detail=error)
    if user.check_against_password(password) is False:
        HTTPException(status_code=401, detail=error)

@router.post("/refresh")
async def refresh_login():
    pass

@router.post("/register")
async def register():
    pass
