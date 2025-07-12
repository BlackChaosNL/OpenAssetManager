from httpx import AsyncClient
from modules.users.models import ACL, Membership
from modules.organizations.models import Organization
from unittest.mock import ANY
from tests.base_test import Test


class TestOrganizationRoute(Test):
    async def test_get_organizations_from_api(
        self, client: AsyncClient, create_user_with_org
    ):
        _, _, _, tokens = await create_user_with_org()

        organizations = await client.get(
            "https://localhost/api/v1/organizations/",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert organizations.status_code == 200
        assert organizations.json() == [
            {
                "created_at": ANY,
                "disabled": False,
                "disabled_at": None,
                "id": ANY,
                "modified_at": ANY,
                "name": "simple organization",
                "type": "home",
                "street_name": None,
                "zip_code": None,
                "state": None,
                "city": None,
                "country": None,
            },
        ]

    async def test_create_organization(self, client: AsyncClient, create_user_with_org):
        _, _, _, tokens = await create_user_with_org()

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
            headers={"Authorization": f"Bearer {tokens.access_token}"},
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

    async def test_delete_organization(self, client: AsyncClient, create_user_with_org):
        _, _, _, tokens = await create_user_with_org()

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
            headers={"Authorization": f"Bearer {tokens.access_token}"},
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
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert deleted_org.status_code == 204

    async def test_cannot_delete_organization_you_are_not_a_part_of(
        self, client: AsyncClient, create_user_with_org
    ):
        _, _, _, tokens = await create_user_with_org()

        organization: Organization = await Organization.create(
            name="My Pretty Organization",
            type="xl_org",
            street_name="Alakaventie 5 A 188",
            zip_code="00920",
            state="uusimaa",
            city="Helsinki",
            country="Finland",
        )

        deleted_org = await client.delete(
            f"https://localhost/api/v1/organizations/{organization.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert deleted_org.status_code == 403

    async def test_delete_membership_of_organization(
        self, client: AsyncClient, create_user_with_org
    ):
        user, _, _, tokens = await create_user_with_org()

        organization: Organization = await Organization.create(
            name="My Pretty Organization",
            type="xl_org",
            street_name="Alakaventie 5 A 188",
            zip_code="00920",
            state="uusimaa",
            city="Helsinki",
            country="Finland",
        )

        acl: ACL = await ACL.create(
            READ=True, WRITE=True, REPORT=True, MANAGE=False, ADMIN=False
        )

        await Membership.create(user=user, organization=organization, acl=acl)

        deleted_org = await client.delete(
            f"https://localhost/api/v1/organizations/{organization.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert deleted_org.status_code == 204

    async def test_update_organization(self, client: AsyncClient, create_user_with_org):
        _, _, _, tokens = await create_user_with_org()

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
            headers={"Authorization": f"Bearer {tokens.access_token}"},
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

        update_org = await client.put(
            f"https://localhost/api/v1/organizations/{org_id}",
            json={
                "name": "My awesome organization",
                "type": "xl_org",
                "street_name": "Alakaventie 5 A 188",
                "zip_code": "00920",
                "state": "uusimaa",
                "city": "Helsinki",
                "country": "Finland",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert update_org.json() == {
            "created_at": ANY,
            "modified_at": ANY,
            "disabled_at": None,
            "id": ANY,
            "name": "My awesome organization",
            "type": "xl_org",
            "street_name": "Alakaventie 5 A 188",
            "zip_code": "00920",
            "state": "uusimaa",
            "city": "Helsinki",
            "country": "Finland",
            "disabled": False,
        }

    async def test_cannot_update_organization_you_are_not_a_part_of(
        self, client: AsyncClient, create_user_with_org
    ):
        _, _, _, tokens = await create_user_with_org()

        organization: Organization = await Organization.create(
            name="My Pretty Organization",
            type="xl_org",
            street_name="Alakaventie 5 A 188",
            zip_code="00920",
            state="uusimaa",
            city="Helsinki",
            country="Finland",
        )

        update_org = await client.put(
            f"https://localhost/api/v1/organizations/{organization.id}",
            json={
                "name": "My awesome organization",
                "type": "xl_org",
                "street_name": "Alakaventie 5 A 188",
                "zip_code": "00920",
                "state": "uusimaa",
                "city": "Helsinki",
                "country": "Finland",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert update_org.status_code == 403
        assert update_org.json() == {
            "detail": "It seems you are not part of the organization or are an admin of the said "
            "organization.",
        }

    async def test_cannot_update_organization_you_are_not_an_admin_of(
        self, client: AsyncClient, create_user_with_org
    ):
        _, organization, _, tokens = await create_user_with_org()

        update_org = await client.put(
            f"https://localhost/api/v1/organizations/{organization.id}",
            json={
                "name": "My awesome organization",
                "type": "xl_org",
                "street_name": "Alakaventie 5 A 188",
                "zip_code": "00920",
                "state": "uusimaa",
                "city": "Helsinki",
                "country": "Finland",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        assert update_org.status_code == 403
        assert update_org.json() == {
            "detail": "It seems you are not part of the organization or are an admin of the said "
            "organization.",
        }
