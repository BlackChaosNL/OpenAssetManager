import pytest  # type: ignore
from httpx import AsyncClient
from config import settings
from unittest.mock import ANY

crypt = settings.CRYPT


class TestAuthentication(object):
    @pytest.mark.asyncio
    async def test_authentication_with_non_existing_user_and_password(
        self, client: AsyncClient
    ):
        response = await client.post(
            "https://localhost/api/v1/auth/",
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
        self, client: AsyncClient, use_admin_account
    ):
        _, _, _, _ = use_admin_account
        response = await client.post(
            "https://localhost/api/v1/auth/",
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
        self, client: AsyncClient, use_admin_account
    ):
        _, _, admin, _ = use_admin_account
        response = await client.post(
            "https://localhost/api/v1/auth/",
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
        self, client: AsyncClient, use_user_account
    ):
        _, _, user, _ = use_user_account
        response = await client.post(
            "https://localhost/api/v1/auth/",
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
        self, client: AsyncClient, use_admin_account
    ):
        _, _, admin, _ = use_admin_account
        token = await client.post(
            "https://localhost/api/v1/auth/",
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
