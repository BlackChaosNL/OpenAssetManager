from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException

from modules.invitations.models import Invite
from modules.users.models import User
from modules.users.utils import get_current_active_user

from tortoise.expressions import Q


router = APIRouter(prefix="/api/v1/Users", tags=["User"])


@router.get("/")
async def get_all_invitations(user: Annotated[User, Depends(get_current_active_user)]):
    pass


@router.get("/accept/{invitation_id}")
async def accept_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
):
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & (Q(receiver=user.username) | Q(receiver=user.email))
    )
    invite.accepted = True
    invite.save()
    return invite



@router.get("/reject/{invitation_id}")
async def reject_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> Invite:
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & (Q(receiver=user.username) | Q(receiver=user.email))
    )
    invite.accepted = False
    invite.save()
    return invite


@router.get("/send")
async def accept_invitation(
    user: Annotated[User, Depends(get_current_active_user)],
):
    pass


@router.get("/cancel/{invitation_id}", status_code=204)
async def accept_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> None:
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & Q(sender=user.id)
    )

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    invite.delete()
