from unittest.mock import ANY
from httpx import AsyncClient
from modules.users.models import ACL, Membership
from tests.base_test import Test


class TestInvitationalRoutes(Test):
    async def test_send_invitations(self, client: AsyncClient, create_user_with_org):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin12@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user1231@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user1231@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user1231@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == [
            {
                "id": ANY,
                "receiver": "user1231@localhost.com",
                "sender": str(admin.id),
                "org_id": str(org.id),
                "message": "Hi! We would like to invite you to our organization.",
                "accepted": False,
                "disabled": False,
                "created_at": ANY,
                "modified_at": ANY,
                "disabled_at": None,
            }
        ]

    async def test_cannot_see_others_invitations(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin99@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user18@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user1231@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user1231@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == []

    async def test_accept_sent_invitations(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin191@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user8@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user8@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user8@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == [
            {
                "id": ANY,
                "receiver": "user8@localhost.com",
                "sender": str(admin.id),
                "org_id": str(org.id),
                "message": "Hi! We would like to invite you to our organization.",
                "accepted": False,
                "disabled": False,
                "created_at": ANY,
                "modified_at": ANY,
                "disabled_at": None,
            }
        ]

        invite_id = user_invites.json()[0]["id"]

        accept_invite = await client.get(
            f"https://localhost/api/v1/invitations/accept/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert accept_invite.status_code == 204

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        # When an invite has been accepted, it should be removed.
        assert user_invites.json() == []

    async def test_decline_sent_invitations(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin11@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user98@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user98@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user98@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == [
            {
                "id": ANY,
                "receiver": "user98@localhost.com",
                "sender": str(admin.id),
                "org_id": str(org.id),
                "message": "Hi! We would like to invite you to our organization.",
                "accepted": False,
                "disabled": False,
                "created_at": ANY,
                "modified_at": ANY,
                "disabled_at": None,
            }
        ]

        invite_id = user_invites.json()[0]["id"]

        accept_invite = await client.get(
            f"https://localhost/api/v1/invitations/decline/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert accept_invite.status_code == 204

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == []

    async def test_prevent_accepting_when_declined_sent_invitations(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin9612@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user11918@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user11918@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user11918@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == [
            {
                "id": ANY,
                "receiver": "user11918@localhost.com",
                "sender": str(admin.id),
                "org_id": str(org.id),
                "message": "Hi! We would like to invite you to our organization.",
                "accepted": False,
                "disabled": False,
                "created_at": ANY,
                "modified_at": ANY,
                "disabled_at": None,
            }
        ]

        invite_id = user_invites.json()[0]["id"]

        accept_invite = await client.get(
            f"https://localhost/api/v1/invitations/decline/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert accept_invite.status_code == 204

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == []

        accept_invite = await client.get(
            f"https://localhost/api/v1/invitations/accept/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert accept_invite.status_code == 403
        assert accept_invite.json() == {
            "detail": "The invitation doesn't exist or you don't have access to it."
        }

    async def test_prevent_declining_when_accepted_sent_invitations(
        self, client: AsyncClient, create_user_with_org
    ):
        admin, org, _, admintokens = await create_user_with_org(
            email="superadmin9712@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )
        _, _, _, usertokens = await create_user_with_org(email="user14918@localhost.com")

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "user14918@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 200
        assert invite.json() == {
            "accepted": False,
            "created_at": ANY,
            "disabled": False,
            "disabled_at": None,
            "id": ANY,
            "message": "Hi! We would like to invite you to our organization.",
            "modified_at": ANY,
            "org_id": str(org.id),
            "receiver": "user14918@localhost.com",
            "sender": str(admin.id),
        }

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == [
            {
                "id": ANY,
                "receiver": "user14918@localhost.com",
                "sender": str(admin.id),
                "org_id": str(org.id),
                "message": "Hi! We would like to invite you to our organization.",
                "accepted": False,
                "disabled": False,
                "created_at": ANY,
                "modified_at": ANY,
                "disabled_at": None,
            }
        ]

        invite_id = user_invites.json()[0]["id"]

        accept_invite = await client.get(
            f"https://localhost/api/v1/invitations/accept/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert accept_invite.status_code == 204

        user_invites = await client.get(
            "https://localhost/api/v1/invitations/",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert user_invites.status_code == 200
        assert user_invites.json() == []

        decline_invite = await client.get(
            f"https://localhost/api/v1/invitations/accept/{invite_id}",
            headers={"Authorization": f"Bearer {usertokens.access_token}"},
        )

        assert decline_invite.status_code == 403
        assert decline_invite.json() == {
            "detail": "The invitation doesn't exist or you don't have access to it."
        }


    async def test_prevent_adding_user_whom_already_belongs_to_your_organization(
        self, client: AsyncClient, create_user_with_org
    ):
        _, org, _, admintokens = await create_user_with_org(
            email="us3r123@localhost.com",
            username="awesomeadmin",
            password="awesomeadmin",
            is_admin=True,
        )

        user, _, _, _ = await create_user_with_org(email="us3r1234@localhost.com")

        await Membership.create(
            user=user,
            organization=org,
            acl=await ACL.create(READ=True)
        )

        invite = await client.post(
            "https://localhost/api/v1/invitations/send",
            json={
                "org_id": str(org.id),
                "receiver": "us3r1234@localhost.com",
                "acl": None,
                "message": "Hi! We would like to invite you to our organization.",
            },
            headers={"Authorization": f"Bearer {admintokens.access_token}"},
        )

        assert invite.status_code == 403
        assert invite.json() == {
            "detail": "The person you've invited is already part of the organization."
        }
