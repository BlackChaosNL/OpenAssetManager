from datetime import datetime
from typing import Annotated
import uuid
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from pydantic import EmailStr
import pytz
from modules.users.utils import get_current_active_user
from modules.auth.utils import create_jwt_tokens, get_tokens_from_logged_in_user
from modules.auth.models import Token
from modules.users.models import User
from fastapi import Depends, HTTPException, status
from tortoise.expressions import Q
from config import settings


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

account_error: str = "E-Mail Address or password is incorrect"
token_error: str = "Refresh token not found or something went wrong."

crypt = settings.CRYPT


@router.post("/")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login

    Logs the user into our API, creates tokens and passes them back to User.
    """
    user: User | None = await User.filter(email=form.username).first()

    if user is None:
        raise HTTPException(status_code=401, detail=account_error)

    if user.check_against_password(form.password) is False:
        raise HTTPException(status_code=401, detail=account_error)

    if user.disabled is True:
        raise HTTPException(status_code=401, detail=account_error)

    tokens = await create_jwt_tokens(user)

    return {"jwt": tokens}


@router.get("/logout", status_code=204)
async def logout(user: Annotated[User, Depends(get_current_active_user)]):
    """
    Logout

    Logout destroys all tokens for User that are currently active. 
    """
    get_all_tokens = await Token.filter(Q(user__id=user.id))
    if get_all_tokens is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="An error occurred."
        )
    for token in get_all_tokens:
        await token.delete()
    return


@router.post("/refresh")
async def refresh_login(
    refresh_token: Annotated[Token | None, Depends(get_tokens_from_logged_in_user)]
):
    """
    Refresh

    After ging this route a token that is active and not disabled, we disable ALL other tokens and pass along new tokens.
    Tokens are alive for about 10 minutes. Refresh tokens are alive for 20 minutes. 
    """
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=token_error,
        )

    # Disable tokens if used after expiration.
    if (
        refresh_token.created_at >= datetime.now(tz=pytz.utc)
        and refresh_token.disabled is False
    ):
        refresh_token.delete()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=token_error,
        )

    if refresh_token.disabled is True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=token_error,
        )

    get_all_tokens = await Token.filter(Q(user__id=refresh_token.user_id))
    
    for token in get_all_tokens:
        if token.id != refresh_token.id:
            await token.delete()
    
    tokens = await create_jwt_tokens(
        user=await User.filter(Q(id=refresh_token.user_id)).first()
    )

    return {"jwt": tokens}


@router.post("/register")
async def register(email: EmailStr, name: str, surname: str, password: str, validate_password: str):
    pass

@router.post("/2fa")
async def twofa():
    pass