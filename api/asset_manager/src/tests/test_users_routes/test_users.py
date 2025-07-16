from tests.base_test import Test
from tortoise.expressions import Q
from tests.base_test import Test
from httpx import AsyncClient
from unittest.mock import ANY
from modules.users.models import User

class TestAccounts(Test):
    async def test_setup_new_account(self, client: AsyncClient):
        # Ensure account is never available. Prevents account already being available.
        check_if_account_exists: User | None = await User.filter(
            Q(email="superuser@localhost.com")
        ).get_or_none()
        if check_if_account_exists:
            await check_if_account_exists.delete(force=True)

        account = await client.post(
            "https://localhost/api/v1/users/",
            json={
                "email": "superuser@localhost.com",
                "username": "superuser",
                "name": "awesome",
                "surname": "superuser",
                "password": "superuserpassword",
                "validate_password": "superuserpassword",
            },
        )

        assert account.status_code == 201
        assert account.json() == {
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "email": "superuser@localhost.com",
            "id": ANY,
            "modified_at": ANY,
            "name": "awesome",
            "surname": "superuser",
            "username": "superuser",
        }

    async def test_me_route(self, client: AsyncClient, create_user_with_org):
        # Ensure account is never available. Prevents account already being available.
        _, _, _, tokens = await create_user_with_org()


        account = await client.get(
            "https://localhost/api/v1/users/me",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert account.status_code == 200
        assert account.json() == {
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "email": "user@localhost.com",
            "id": ANY,
            "modified_at": ANY,
            "name": "awesome",
            "surname": "user",
            "username": "user",
        }