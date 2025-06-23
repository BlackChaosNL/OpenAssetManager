from modules.users.models import User
import pytest  # type: ignore
from httpx import AsyncClient
from config import settings
from unittest.mock import ANY
from tortoise.expressions import Q

crypt = settings.CRYPT


class TestAuthentication(object):
    @pytest.mark.asyncio
    async def test_authentication_with_non_existing_user_and_password(
        self, client: AsyncClient
    ):
        response = await client.post(
            "https://localhost/api/v1/auth/login",
            data={
                "username": "non-existing@localhost.com",
                "password": "password",
                "grant_type": "password",
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "E-Mail Address or password is incorrect"}

    @pytest.mark.asyncio
    async def test_authentication_with_existing_user_and_wrong_password(
        self, client: AsyncClient, create_user_with_org
    ):
        _, _, _, _ = await create_user_with_org()
        response = await client.post(
            "https://localhost/api/v1/auth/login",
            data={
                "username": "admin@localhost.com",
                "password": "password",
                "grant_type": "password",
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "E-Mail Address or password is incorrect"}

    @pytest.mark.asyncio
    async def test_authentication_with_existing_user_and_password(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, _, _, _ = await create_user_with_org(email="admin@localhost.com", password="adminpassword")
        response = await client.post(
            "https://localhost/api/v1/auth/login",
            data={
                "username": "admin@localhost.com",
                "password": "adminpassword",
                "grant_type": "password",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "jwt": {
                "created_at": ANY,
                "user_id": str(admin.id),
                "id": ANY,
                "modified_at": ANY,
                "disabled_at": None,
                "refresh_token": ANY,
                "disabled": False,
                "access_token": ANY,
                "token_type": "Bearer",
            }
        }

    @pytest.mark.asyncio
    async def test_logging_out_destroys_tokens(
        self, client: AsyncClient, create_user_with_org
    ):
        user, _, _, _ = await create_user_with_org(email="user@localhost.com", password="userpassword")
        response = await client.post(
            "https://localhost/api/v1/auth/login",
            data={
                "username": "user@localhost.com",
                "password": "userpassword",
                "grant_type": "password",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "jwt": {
                "created_at": ANY,
                "user_id": str(user.id),
                "id": ANY,
                "modified_at": ANY,
                "disabled_at": None,
                "refresh_token": ANY,
                "disabled": False,
                "access_token": ANY,
                "token_type": "Bearer",
            }
        }

        access_token = response.json()["jwt"]["access_token"]
        refresh_token = response.json()["jwt"]["refresh_token"]

        logout = await client.get(
            "https://localhost/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert logout.status_code == 204

        refresh_request = await client.post(
            "https://localhost/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        assert refresh_request.status_code == 401
        assert refresh_request.json() == {
            "detail": "Refresh token not found or something went wrong."
        }

    @pytest.mark.asyncio
    async def test_create_new_tokens_upon_refresh(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, _, _, _ = await create_user_with_org(email="admin@localhost.com", password="adminpassword")
        token = await client.post(
            "https://localhost/api/v1/auth/login",
            data={
                "username": "admin@localhost.com",
                "password": "adminpassword",
                "grant_type": "password",
            },
        )
        assert token.status_code == 200
        assert token.json() == {
            "jwt": {
                "created_at": ANY,
                "user_id": str(admin.id),
                "id": ANY,
                "modified_at": ANY,
                "disabled_at": None,
                "refresh_token": ANY,
                "disabled": False,
                "access_token": ANY,
                "token_type": "Bearer",
            }
        }

        refresh_token = token.json()["jwt"]["refresh_token"]

        response2 = await client.post(
            "https://localhost/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        assert response2.status_code == 200
        assert response2.json() == {
            "jwt": {
                "created_at": ANY,
                "user_id": str(admin.id),
                "id": ANY,
                "modified_at": ANY,
                "disabled_at": None,
                "refresh_token": ANY,
                "disabled": False,
                "access_token": ANY,
                "token_type": "Bearer",
            }
        }

    @pytest.mark.asyncio
    async def test_setup_new_account(self, client: AsyncClient):
        # Ensure account is never available. Prevents account already being available.
        check_if_account_exists: User | None = await User.filter(
            Q(email="superuser@localhost.com")
        ).get_or_none()
        if check_if_account_exists:
            await check_if_account_exists.delete(force=True)

        account = await client.post(
            "https://localhost/api/v1/auth/register",
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
