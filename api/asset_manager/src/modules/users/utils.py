from typing import Annotated
from joserfc import jwt  # type: ignore
from joserfc.jwk import OctKey  # type: ignore

from tortoise.expressions import Q
from fastapi import Depends, HTTPException, status

from modules.users.models import User
from config import settings


async def get_user_from_token(
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

    return await User.filter(Q(id=user_id)).first()


async def get_current_active_user(
    user: Annotated[User | None, Depends(get_user_from_token)],
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not found or active",
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not found or active",
        )
    return user
