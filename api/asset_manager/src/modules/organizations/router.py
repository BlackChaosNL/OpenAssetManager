import uuid
from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from modules.organizations.models import Organization
from modules.organizations.schemas import organization_model, register_organization
from modules.users.utils import get_current_active_user
from modules.users.models import ACL, Membership, User
from tortoise.expressions import Q

router = APIRouter(prefix="/api/v1/organizations", tags=["orgs"])


@router.get("/", response_model=List[organization_model])
async def all_active_organizations(
    user: Annotated[User, Depends(get_current_active_user)],
) -> List[Organization]:
    memberships: List[Membership] = list(
        await Membership.filter(
            Q(user_id=user.id) & Q(disabled=False)
        ).prefetch_related("organization")
    )
    organizations: List[Organization] = []

    if len(memberships) < 1:
        raise HTTPException(status_code=404, detail="No active organizations found!")

    for member in memberships:
        organizations.append(member.organization)

    return organizations


@router.delete("/{org_id}", status_code=204)
async def delete_organization(
    user: Annotated[User, Depends(get_current_active_user)], org_id: uuid.UUID
) -> None:
    membership: Membership | None = (
        await Membership.filter(Q(user_id=user.id) & Q(organization_id=org_id))
        .get_or_none()
        .prefetch_related("acl", "user", "organization")
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not part of the organization you wish to leave or remove.",
        )

    if membership.acl.ADMIN:
        # Prepare to remove ALL members in the organization.
        # We've already checked whether user is ADMIN.
        all_memberships: List[Membership] = list(
            await Membership.filter(Q(organization_id=org_id)).prefetch_related(
                "acl", "user", "organization"
            )
        )
        for member in all_memberships:
            await member.acl.delete()
            await member.delete()
        # Completely remove organization.
        await membership.organization.delete()
    else:
        await membership.delete()
    return


@router.post("/", response_model=organization_model)
async def create_organization(
    user: Annotated[User, Depends(get_current_active_user)],
    register_organization: register_organization,
) -> Organization:
    acl: ACL = await ACL.create(
        READ=True, WRITE=True, REPORT=True, MANAGE=True, ADMIN=True
    )

    org: Organization = await Organization.create(
        name=register_organization.name,
        type=register_organization.type,
        street_name=register_organization.street_name,
        zip_code=register_organization.zip_code,
        state=register_organization.state,
        city=register_organization.city,
        country=register_organization.country,
    )

    await Membership.create(organization=org, user=user, acl=acl)
    return org


@router.put("/{org_id}", response_model=organization_model)
async def update_organization(
    user: Annotated[User, Depends(get_current_active_user)],
    org_id: uuid.UUID,
    alter_organization: register_organization,
) -> Organization:
    org: Organization | None = Organization.filter(
        Q(users__id=user.id) & Q(id=org_id)
    ).get_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization could not be found.")
    return await org.update_from_dict(**alter_organization)
