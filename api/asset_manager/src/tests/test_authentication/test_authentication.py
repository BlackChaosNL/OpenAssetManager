import pytest  # type: ignore
from httpx import AsyncClient
from config import settings

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
        response = await client.post(
            "http://localhost/api/v1/auth/",
            data={
                "username": "admin@localhost.com",
                "password": "adminpassword",
                "grant_type": "password",
            },
        )
        assert response.status_code == 200
        assert response.text == ""
