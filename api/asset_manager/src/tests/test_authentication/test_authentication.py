from tests.fixtures.conftest import init_db
import pytest
from fastapi.testclient import TestClient
from modules.organizations.models import Organization
from modules.users.models import ACL, Membership, User
from main import app
from config import settings

client = TestClient(app)

crypt = settings.CRYPT


async def setup_function():
    init_db()
    org = await Organization.create(name="Admin's Organization", type="home")
    user = await User.create(
        email="admin@localhost.com",
        username="admin",
        name="admin",
        surname="admin",
    )
    user.set_password("password")
    user.save()
    acl = await ACL.create(READ=True, WRITE=True, REPORT=True, MANAGE=True, ADMIN=True)
    await Membership.create(organization=org, user=user, acl=acl)

    print(org, user, acl)


# def teardown_function():
#     Organization.all().delete()
#     User.all().delete()
#     ACL.all().delete()
#     Membership.all().delete()


def test_read_main():
    response = client.post(
        "/api/v1/auth",
        data={
            "username": "admin@localhost.com",
            "password": "password",
            "grant_type": "password",
        },
    )
    assert response.json() == {}
    assert response.status_code == 200
