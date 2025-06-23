
import pytest
from dataclasses import dataclass
from modules.auth.utils import create_jwt_tokens
from modules.organizations.models import Organization, OrganizationType
from modules.users.models import ACL, Membership, User
from modules.auth.models import Token

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
        org: Organization = await Organization.create(
            name=organization_name,
            type=organization_type
        )

        acl: ACL = await ACL.create(
            READ=True,
            WRITE=True,
            REPORT=True,
            MANAGE=True if is_admin else False,
            ADMIN=True if is_admin else False,
        )

        user: User = await User.create(
            email=email,
            username=username,
            name=name,
            surname=surname,
            password=crypt.hash(password),
        )

        await Membership.create(
            organization=org,
            user=user,
            acl=acl
        )

        tokens: Token = await create_jwt_tokens(user=user)

        return user, org, acl, tokens
    return inner_function