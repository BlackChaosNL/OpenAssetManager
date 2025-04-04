import pytest  # type: ignore
from httpx import AsyncClient
from config import settings
from unittest.mock import ANY

crypt = settings.CRYPT


class TestOrganizationRoute(object):
    @pytest.mark.asyncio
    async def test_get_organizations_from_api(
        self, client: AsyncClient, get_admin_login_token
    ):
        access_token, _ = get_admin_login_token

        organizations = await client.get(
            "https://localhost/api/v1/organizations/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert organizations.status_code == 200
        assert organizations.json() == [
            {
                "created_at": ANY,
                "disabled": False,
                "disabled_at": None,
                "id": ANY,
                "modified_at": ANY,
                "name": "Superadmin's Organization",
                "type": "non_profit",
                "street_name": None,
                "zip_code": None,
                "state": None,
                "city": None,
                "country": None,
            },
        ]

    @pytest.mark.asyncio
    async def test_create_organization(
        self, client: AsyncClient, get_user_login_token
    ):
        access_token, _ = get_user_login_token

        organizations = await client.post(
            "https://localhost/api/v1/organizations/",
            json={
                "name": "My new organization",
                "type": "xl_org",
                "street_name": "Alakaventie 5 A 188",
                "zip_code": "00920",
                "state": "uusimaa",
                "city": "Helsinki",
                "country": "Finland",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert organizations.status_code == 200
        assert organizations.json() == {
            "created_at": ANY,
            "modified_at": ANY,
            "disabled_at": None,
            "id": ANY,
            "name": "My new organization",
            "type": "xl_org",
            "street_name": "Alakaventie 5 A 188",
            "zip_code": "00920",
            "state": "uusimaa",
            "city": "Helsinki",
            "country": "Finland",
            "disabled": False,
        }

    @pytest.mark.asyncio
    async def test_delete_organization(
        self, client: AsyncClient, get_user_login_token
    ):
        access_token, _ = get_user_login_token

        organizations = await client.post(
            "https://localhost/api/v1/organizations/",
            json={
                "name": "My new organization",
                "type": "xl_org",
                "street_name": "Alakaventie 5 A 188",
                "zip_code": "00920",
                "state": "uusimaa",
                "city": "Helsinki",
                "country": "Finland",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert organizations.status_code == 200
        assert organizations.json() == {
            "created_at": ANY,
            "modified_at": ANY,
            "disabled_at": None,
            "id": ANY,
            "name": "My new organization",
            "type": "xl_org",
            "street_name": "Alakaventie 5 A 188",
            "zip_code": "00920",
            "state": "uusimaa",
            "city": "Helsinki",
            "country": "Finland",
            "disabled": False,
        }

        org_id = organizations.json()["id"]

        deleted_org = await client.delete(
            f"https://localhost/api/v1/organizations/{org_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert deleted_org.status_code == 204


    # @pytest.mark.asyncio
    # async def test_update_organization(
    #     self, client: AsyncClient, get_admin_login_token
    # ):
    #     access_token, _ = get_admin_login_token

    #     organizations = await client.post(
    #         "https://localhost/api/v1/organizations/",
    #         json={
    #             "name": "My new organization",
    #             "type": "xl_org",
    #             "street_name": "Alakaventie 5 A 188",
    #             "zip_code": "00920",
    #             "state": "uusimaa",
    #             "city": "Helsinki",
    #             "country": "Finland",
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     assert organizations.status_code == 200
    #     assert organizations.json() == {
    #         "created_at": ANY,
    #         "modified_at": ANY,
    #         "disabled_at": None,
    #         "id": ANY,
    #         "name": "My new organization",
    #         "type": "xl_org",
    #         "street_name": "Alakaventie 5 A 188",
    #         "zip_code": "00920",
    #         "state": "uusimaa",
    #         "city": "Helsinki",
    #         "country": "Finland",
    #         "disabled": False,
    #     }

    #     org_id = organizations.json()["id"]

    #     update_org = await client.put(
    #         f"https://localhost/api/v1/organizations/{org_id}",
    #         json={
    #             "name": "My awesome organization",
    #         },
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )

    #     assert update_org.json() == {
    #         "created_at": ANY,
    #         "modified_at": ANY,
    #         "disabled_at": None,
    #         "id": ANY,
    #         "name": "My new organization",
    #         "type": "xl_org",
    #         "street_name": "Alakaventie 5 A 188",
    #         "zip_code": "00920",
    #         "state": "uusimaa",
    #         "city": "Helsinki",
    #         "country": "Finland",
    #         "disabled": False,
    #     }