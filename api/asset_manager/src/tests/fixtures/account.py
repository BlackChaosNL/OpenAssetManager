
import pytest
from dataclasses import dataclass
from modules.auth.utils import create_jwt_tokens
from modules.organizations.models import Organization, OrganizationType
from modules.users.models import ACL, Membership, User
from modules.auth.models import Token
from tortoise.expressions import Q

from config import settings

crypt = settings.CRYPT

@dataclass
class user_creation_return_type:
    user: User
    organization: Organization
    acl: ACL
    tokens: Token

@pytest.fixture()
async def create_user_with_org():
    async def inner_function(email="user@localhost.com", 
                             username="user",
                             name="awesome",
                             surname="user",
                             password="password-dont-use",
                             organization_name="simple organization",
                             organization_type=OrganizationType.HOME,
                             is_admin=False) -> user_creation_return_type:
        org: Organization | None = await Organization.filter(Q(name=organization_name) & Q(name=organization_type)).first()
        if not org:
            org: Organization = await Organization.create(
                name=organization_name,
                type=organization_type
            )

        user: User | None = await User.filter(Q(email=email)).first()
        if not user:
            user: User = await User.create(
                email=email,
                username=username,
                name=name,
                surname=surname,
                password=crypt.hash(password),
            )

        acl: ACL | None = await ACL.filter(Q(id="5f33facd-08dd-48a1-8f15-3b24f2a727f5")).first()
        if not acl:
            acl: ACL = await ACL.create(
                id="5f33facd-08dd-48a1-8f15-3b24f2a727f5",
                READ=True,
                WRITE=True,
                REPORT=True,
                MANAGE=True if is_admin else False,
                ADMIN=True if is_admin else False,
            )

        membership: Membership | None = await Membership.filter(Q(user=user, organization=org, acl=acl)).first()
        if not membership:
            await Membership.get_or_create(
                organization=org,
                user=user,
                acl=acl
            )

        tokens: Token = await create_jwt_tokens(user=user)

        return user, org, acl, tokens
    return inner_function