from modules.organizations.models import Organization, OrganizationType
from modules.users.models import ACL, Membership, User
import pytest  # type: ignore
from config import settings

crypt = settings.CRYPT


@pytest.fixture()
async def use_user_account():
    org, _ = await Organization.get_or_create(
        id="6ad4c94e-0522-4912-8d16-02d451f4c92d",
        name="User's Organization",
        type=OrganizationType.HOME,
    )
    acl, _ = await ACL.get_or_create(
        id="a4e927a3-36e5-4761-badb-0a44ade6616f",
        READ=True,
        WRITE=True,
        REPORT=True,
        MANAGE=False,
        ADMIN=False,
    )
    user, _ = await User.get_or_create(
        id="24235427-9662-4ba3-a9c5-00000000000b",
        email="user@localhost.com",
        username="user",
        name="awesome",
        surname="user",
        password=crypt.hash("userpassword"),
    )
    membership, _ = await Membership.get_or_create(
        id="833b9511-b2da-4760-8fa4-1a5c7059911e",
        organization=org,
        user=user,
        acl=acl,
    )
    return org, acl, user, membership


@pytest.fixture()
async def use_admin_account():
    org, _ = await Organization.get_or_create(
        id="de001f44-1bb8-4667-9f9d-2d62d6ad7270",
        name="Admin's Organization",
        type=OrganizationType.EXTRA_LARGE_ORGANIZATION,
    )
    acl, _ = await ACL.get_or_create(
        id="83c1bfe6-c2ed-4ba1-be03-0e5c1960ec31",
        READ=True,
        WRITE=True,
        REPORT=True,
        MANAGE=True,
        ADMIN=True,
    )
    user, _ = await User.get_or_create(
        defaults={
            "id": "24235427-9662-4ba3-a9c5-00000000000a",
            "email": "admin@localhost.com",
            "username": "admin",
            "name": "awesome",
            "surname": "admin",
            "password": crypt.hash("adminpassword"),
        }
    )
    membership, _ = await Membership.get_or_create(
        id="393473ee-c218-4bcf-82cd-cb676c4d8a33",
        organization=org,
        user=user,
        acl=acl,
    )
    return org, acl, user, membership
