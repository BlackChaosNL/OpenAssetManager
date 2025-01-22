from datetime import timedelta
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.routing import APIRouter
from utils import create_token, crypt_password
from models import Token
from modules.users.models import User
from fastapi import Depends, HTTPException
from config import settings
from tortoise.expressions import Q
from schemas import TokenModel


router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

error: str = "E-Mail Address or password is incorrect"

crypt = settings.CRYPT


@router.post("/", response_model=TokenModel)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: User = await User.filter(
        Q(email=form.username) & Q(password=crypt_password(form.password))
    ).get_or_none()

    if user is None:
        HTTPException(status_code=401, detail=error)

    if user.check_against_password(form.password) is False:
        HTTPException(status_code=401, detail=error)

    return JSONResponse(
        await Token.create(
            user=f"id:{user.id}",
            access_token=create_token(
                user_id=user.id, offset=timedelta(settings.ACCESS_TOKEN_EXPIRE_MIN)
            ),
            refresh_token=create_token(
                user_id=user.id, offset=timedelta(settings.REFRESH_TOKEN_EXPIRE_MIN)
            ),
        )
    )


@router.post("/refresh")
async def refresh_login():
    pass


@router.post("/register")
async def register():
    pass
