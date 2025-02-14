import uuid
from modules.organizations.models import Organization
from modules.users.models import ACL, Membership, User
import pytest # type: ignore
from config import settings

crypt = settings.CRYPT

@pytest.fixture()
async def use_user_account():
        org = await Organization.create(name="User's Organization", type="home")
        acl = await ACL.create(
            READ=True, WRITE=True, REPORT=True, MANAGE=True, ADMIN=True
        )
        user = await User.create(
            email="user@localhost.com",
            username="user",
            name="awesome",
            surname="user",
            password=crypt.hash("userpassword"),
        )
        membership = await Membership.create(
            organization=org,
            user=user,
            acl=acl,
        )
        return org, acl, user, membership

@pytest.fixture()
async def use_admin_account():
        org = await Organization.create(name="Admin's Organization", type="home")
        acl = await ACL.create(
            READ=True, WRITE=True, REPORT=True, MANAGE=True, ADMIN=True
        )
        user = await User.create(
            email="admin@localhost.com",
            username="admin",
            name="awesome",
            surname="admin",
            password=crypt.hash("adminpassword"),
        )
        membership = await Membership.create(
            organization=org,
            user=user,
            acl=acl,
        )
        return org, acl, user, membership

