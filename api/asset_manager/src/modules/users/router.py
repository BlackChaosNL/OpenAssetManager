from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi import HTTPException, status

from tortoise.expressions import Q

from modules.users.utils import get_current_active_user
from modules.auth.schemas import register_model
from modules.users.models import User
from modules.users.schemas import user_model

from config import settings


router = APIRouter(prefix="/api/v1/users", tags=["users"])

crypt = settings.CRYPT

user_exists: str = "Account failed to create, please contact support."
password_failed: str = "Password validation failed, please try again."


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_model)
async def create_user(user: register_model):
    # Prevent existing users from reapplying for our system.
    existing_user: User | None = await User.filter(
        Q(email=user.email)
        & Q(username=user.username)
        & Q(name=user.name)
        & Q(surname=user.surname)
    ).get_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user_exists,
        )

    if user.password != user.validate_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=password_failed,
        )

    return await User.create(
        email=user.email,
        username=user.username,
        name=user.name,
        surname=user.surname,
        password=crypt.hash(user.password),
    )


@router.get("/me", response_model=user_model)
async def get_user(user: Annotated[User, Depends(get_current_active_user)]):
    return user
