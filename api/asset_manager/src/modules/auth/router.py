from datetime import timedelta
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.routing import APIRouter
from modules.auth.utils import create_token
from modules.auth.models import Token
from modules.users.models import User
from fastapi import Depends, HTTPException
from config import settings
from tortoise.expressions import Q


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

error: str = "E-Mail Address or password is incorrect"

crypt = settings.CRYPT


@router.post("/")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: User | None = await User.filter(
        Q(email=form.username)
    ).get_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail=error)

    if user.check_against_password(form.password) is False:
        raise HTTPException(status_code=401, detail=error)

    return JSONResponse(
        await Token.create(
            user=user.id,
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
