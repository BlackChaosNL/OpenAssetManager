import pytest
from httpx import AsyncClient
from modules.organizations.models import Organization
from modules.users.models import ACL, Membership, User
from config import settings
crypt = settings.CRYPT

@pytest.mark.anyio
async def setup_function():
    org = await Organization.create(name="Admin's Organization", type="home")
    user = await User.create(
        email="admin@localhost.com",
        username="admin",
        name="admin",
        surname="admin",
        password=crypt.hash("password")
    )
    acl = await ACL.create(READ=True, WRITE=True, REPORT=True, MANAGE=True, ADMIN=True)
    await Membership.create(organization=org, user=user, acl=acl)


# def teardown_function():
#     Organization.all().delete()
#     User.all().delete()
#     ACL.all().delete()
#     Membership.all().delete()

async def test_read_main(client: AsyncClient):
    print("start")
    response = await client.post(
        "http://localhost/api/v1/auth",
        data={
            "username": "admin@localhost.com",
            "password": "password",
            "grant_type": "password",
        },
    )
    assert response.json() == {}
    assert response.status_code == 200
