from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from modules.organizations.models import Organization
from modules.invitations.models import Invite
from modules.invitations.schemas import invitation_model, send_invitation_for_org

from modules.users.models import ACL, Membership, User
from modules.users.utils import get_current_active_user

from tortoise.expressions import Q

router = APIRouter(prefix="/api/v1/invitations", tags=["invites"])


@router.get("/", response_model=List[invitation_model])
async def get_all_invitations(
    user: Annotated[User, Depends(get_current_active_user)],
) -> List[Invite]:
    """Returns all invitations for user requesting, except disabled invites.

    Args:
        user (Annotated[User, Depends(get_current_active_user)]): Returns user token.

    Returns:
        List[Invite]: A list of invitations.
    """
    return await Invite.filter(
        Q(receiver=user.username) | Q(receiver=user.email) & Q(disabled=False)
    )


@router.delete("/{invitation_id}", response_model=invitation_model)
async def delete_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> None:
    """Removes an invitation you have sent

    Args:
        user (Annotated[User, Depends(get_current_active_user)]): Returns user token.
        invitation_id (uuid.UUID): UUID for the invitation to be removed

    Raises:
        HTTPException: When invitation doesn't exist return 403.

    Returns:
        Invite: The Invitation model.
    """
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id) & Q(sender=user.id) & Q(disabled=False)
    )

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    await invite.delete()
    return invite


@router.get("/accept/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def accept_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> None:
    """Accepts the invitation sent by a different organization.

    Args:
        user (Annotated[User, Depends(get_current_active_user)]): Returns user token.
        invitation_id (uuid.UUID): UUID for the organization that the users wants to add the person to.

    Raises:
        HTTPException: Raises exception when invite is not available or disabled.

    """
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id)
        & (Q(receiver=user.username) | Q(receiver=user.email))
        & Q(disabled=False)
    ).prefetch_related("acl")

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    if invite.disabled:
        raise HTTPException(
            status_code=403,
            detail="You have already declined the invitation or the invitation was removed, you can't accept it.",
        )

    invite.accepted = True
    await invite.save()
    # Disable invite after accepting, prevent changing it.
    await invite.delete()

    await Membership.create(
        user=user, organization=await Organization.get(id=invite.org_id), acl=invite.acl
    )


@router.get("/decline/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def reject_invitation(
    user: Annotated[User, Depends(get_current_active_user)], invitation_id: uuid.UUID
) -> None:
    """Declines an invitation to join an organization

    Args:
        user (Annotated[User, Depends(get_current_active_user)]): Returns user token.
        invitation_id (uuid.UUID): The UUID of the invitation

    Raises:
        HTTPException: Checks if the invite exists.
        HTTPException: Checks if the invite has already accepted.

    Returns:
        Invite: The Invitation model.
    """
    invite: Invite | None = await Invite.get_or_none(
        Q(id=invitation_id)
        & (Q(receiver=user.username) | Q(receiver=user.email))
        & Q(disabled=False)
    ).prefetch_related("acl")

    if not invite:
        raise HTTPException(
            status_code=403,
            detail="The invitation doesn't exist or you don't have access to it.",
        )

    if invite.accepted:
        raise HTTPException(
            status_code=403,
            detail="The invitation was already accepted, you can't remove it.",
        )

    await invite.delete()


@router.post("/send", response_model=invitation_model)
async def send_invitation(
    user: Annotated[User, Depends(get_current_active_user)],
    invite_details: send_invitation_for_org,
) -> Invite:
    """Sends an invitation to e-mail or username.

    Args:
        user (Annotated[User, Depends(get_current_active_user)]): Returns user token.
        invite_details (send_invitation_for_org): The details for the invitation.

    Raises:
        HTTPException: Checks access to the organization posted.
        HTTPException: Checks for Manager or Admin permissions and declines if you are not.

    Returns:
        Invite: The Invitation model.
    """
    # Should send an E-Mail as notification.
    membership = await Membership.get_or_none(
        Q(user=user.id) & Q(organization=invite_details.org_id)
    ).prefetch_related("acl")

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this organization.",
        )

    if not membership.acl.MANAGE or not membership.acl.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to send invitations for this organization.",
        )

    # Check if user is already part of organization
    invited_user: User | None = await User.get_or_none(
        Q(username=invite_details.receiver) | Q(email=invite_details.receiver)
    )

    if invited_user:
        user_is_part_of_org = await Membership.get_or_none(
            Q(user=invited_user) & Q(organization=invite_details.org_id)
        )
        if user_is_part_of_org:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The person you've invited is already part of the organization.",
            )

    acl = None
    if invite_details.acl:
        acl = await ACL.create(
            READ=invite_details.acl.READ,
            WRITE=invite_details.acl.WRITE,
            REPORT=invite_details.acl.REPORT,
            MANAGE=invite_details.acl.MANAGE,
            ADMIN=invite_details.acl.ADMIN,
        )
    else:
        acl = await ACL.create(
            READ=True,
        )

    return await Invite.create(
        receiver=invite_details.receiver,
        sender=user.id,
        org_id=invite_details.org_id,
        message=invite_details.message,
        acl=acl,
    )
