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
            "http://localhost/api/v1/auth/",
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
            "http://localhost/api/v1/auth/",
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
            "http://localhost/api/v1/auth/",
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
