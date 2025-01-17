from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.routing import APIRouter
from modules.users.models import User
from fastapi import Depends, HTTPException
from config import settings
from tortoise.expressions import Q
from authlib.jose import jwt  # type: ignore

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MIN

error: str = "E-Mail Address or password is incorrect"

crypt = settings.CRYPT


@router.post("/")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: User = await User.filter(Q(email=form.username)).get_or_none()

    if user is None:
        HTTPException(status_code=401, detail=error)

    if user.check_against_password(form.password) is False:
        HTTPException(status_code=401, detail=error)


@router.post("/refresh")
async def refresh_login():
    pass


@router.post("/register")
async def register():
    pass
