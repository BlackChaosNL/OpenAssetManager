from typing import Annotated, List
from fastapi import APIRouter, Depends

from fastapi import HTTPException, status

from tortoise.expressions import Q

from modules.auth.models import Token
from modules.users.utils import get_current_active_user
from modules.users.schemas import register_model, update_user_model
from modules.users.models import Membership, User
from modules.users.schemas import user_model

from config import settings


router = APIRouter(prefix="/api/v1/users", tags=["users"])

crypt = settings.CRYPT

user_exists: str = "Account failed to create, please contact support."
password_failed: str = "Password validation failed, please try again."


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_model)
async def create_user(user: register_model):
    # Prevent existing users from reapplying for our system.
    existing_user: User | None = await User.get_or_none(
        Q(email=user.email)
        & Q(username=user.username)
        & Q(name=user.name)
        & Q(surname=user.surname)
        & Q(disabled=False)
    )

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


@router.put("/me", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user: Annotated[User, Depends(get_current_active_user)],
    updated_user: update_user_model,
):
    if updated_user.email:
        user.email = updated_user.email
    if updated_user.name:
        user.name = updated_user.name
    if updated_user.surname:
        user.surname = updated_user.surname

    if (
        updated_user.old_password
        and updated_user.password
        and updated_user.validate_password
    ):
        user.update_password(
            updated_user.old_password,
            updated_user.password,
            updated_user.validate_password,
        )

    await user.save()


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user: Annotated[User, Depends(get_current_active_user)],
):
    memberships: List[Membership] = await Membership.filter(Q(user__id=user.id) & Q(disabled=False))
    for membership in memberships:
        await membership.acl.delete()
        await membership.delete()
    tokens: List[Token] = await Token.filter(Q(user__id=user.id) & Q(disabled=False))
    for token in tokens:
        await token.delete()
    await user.delete()


@router.get("/me", response_model=user_model)
async def get_user(user: Annotated[User, Depends(get_current_active_user)]):
    return user
