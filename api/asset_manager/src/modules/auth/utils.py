from datetime import timedelta
from typing import Annotated
import uuid, time

from tortoise.expressions import Q
from fastapi import Depends, HTTPException, status

from modules.users.models import User
from modules.auth.models import Token
from config import settings
from joserfc import jwt  # type: ignore
from joserfc.jwk import OctKey  # type: ignore
from config import settings

crypt = settings.CRYPT


def create_token(user_id: uuid, offset: timedelta) -> str:
    """
    Creates a JWT token
    """
    user = str(user_id)
    curr_time = int(time.time())

    return jwt.encode(
        {"alg": "HS256", "typ": "JWT"},
        {
            "iss": f"{settings.PROJECT_PUBLIC_URL}",
            "sub": f"id:{user}",
            "nbf": curr_time,
            "iat": curr_time,
            "exp": int(time.time() + offset.total_seconds()),
        },
        OctKey.import_key(settings.SECRET_KEY),
    )


async def create_jwt_tokens(user: User) -> Token:
    """
    Create a Token class with the following entities:

    1) A user that is attached to the Token
    2) A fresh Auth Token
    3) A fresh Refresh Token.

    This is then returned in the form of an Token class.
    """
    auth_token = create_token(
        user_id=user.id, offset=timedelta(settings.ACCESS_TOKEN_EXPIRE_MIN)
    )

    refresh_token = create_token(
        user_id=user.id, offset=timedelta(settings.REFRESH_TOKEN_EXPIRE_MIN)
    )

    return await Token.create(
        user=user,
        access_token=auth_token,
        refresh_token=refresh_token,
    )


async def get_tokens_from_logged_in_user(
    token: Annotated[str, Depends(settings.OAUTH2_SCHEME)]
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="An issue occurred with the token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: jwt.Token = jwt.decode(
            token, OctKey.import_key(settings.SECRET_KEY), algorithms=["HS256"]
        )
        id: str | None = payload.claims.get("sub", None)
        if id is None:
            raise credentials_exception
        user_id = id.split(":")[1]
    except:
        raise credentials_exception

    return await Token.filter(Q(refresh_token=token) & Q(user__id=user_id)).first()
