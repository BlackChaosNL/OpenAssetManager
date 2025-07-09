from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException

from modules.invitations.models import Invite
from modules.invitations.schemas import invitation_model

from modules.users.models import User
from modules.users.utils import get_current_active_user

from tortoise.expressions import Q


router = APIRouter(prefix="/api/v1/Users", tags=["User"])


@router.get("/", response_model=List[invitation_model])
async def get_all_invitations(
    user: Annotated[User, Depends(get_current_active_user)],
) -> List[Invite]:
    invites: List[Invite] | None = await Invite.filter(
        Q(receiver=user.username) | Q(receiver=user.email)
    )

    return invites


@router.get("/accept/{invitation_id}", response_model=invitation_model)
async def accept_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> Invite:
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & (Q(receiver=user.username) | Q(receiver=user.email))
    )

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    invite.accepted = True
    return await invite.save()


@router.get("/reject/{invitation_id}", response_model=invitation_model)
async def reject_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> Invite:
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & (Q(receiver=user.username) | Q(receiver=user.email))
    )

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    invite.accepted = False
    return await invite.save()


@router.get("/send")
async def send_invitation(
    user: Annotated[User, Depends(get_current_active_user)],
):
    # Check if user is Manager or Higher to send an invitation.
    # Should send an E-Mail as notification.
    pass


@router.get("/cancel/{invitation_id}", response_model=invitation_model)
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

    return await invite.delete()
