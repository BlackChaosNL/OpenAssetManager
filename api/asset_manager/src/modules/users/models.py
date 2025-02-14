from datetime import datetime
import uuid
from pydantic import EmailStr
from tortoise.models import Model
from tortoise import fields

from modules.organizations.models import Organization
from mixins.CMDMixin import CMDMixin
from config import settings

crypt = settings.CRYPT

class User(Model, CMDMixin):
    """
    User

    This holds all of our users
    """

    id: uuid = fields.UUIDField(primary_key=True)
    email: EmailStr = fields.CharField(max_length=128)
    username: str = fields.TextField(max_length=128)
    name: str = fields.TextField(max_length=128)
    surname: str = fields.TextField(max_length=128)
    password: str = fields.CharField(max_length=128, null=True)
    organizations: uuid = fields.ManyToManyField(
        "models.Organization",
        related_name="members",
        through="Membership",
        forward_key="organization_id",
        backward_key="user_id",
        null=True,
        on_delete=fields.NO_ACTION,
    )
    disabled: bool = fields.BooleanField(default=False)
    # tokens = fields.ForeignKeyField("models.Token")

    def __str__(self) -> str:
        return f"{self.id} - {self.name} {self.surname}"

    def set_password(self, password: str) -> None:
        self.password = crypt.hash(
            password
        )
        self.save()  # Make sure to save the model in DB

    def check_against_password(self, password: str) -> bool:
        return crypt.verify(
            password,
            self.password
        )
    
    def update_password(self, old_password, new_password: str, verify_new_password: str) -> bool:
        if self.check_against_password(old_password) is False:
            return False
        if new_password is not verify_new_password:
            return False
        self.set_password(new_password)

    def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=settings.DEFAULT_TIMEZONE)
        self.save()



class ACL(Model):
    """
    ACL

    Access control lists, every invited user gets an ACL and this decides whether you grant / deny access to certain parts of our system.
    """

    id: uuid = fields.UUIDField(primary_key=True)
    READ: bool = fields.BooleanField(default=False)
    WRITE: bool = fields.BooleanField(default=False)
    REPORT: bool = fields.BooleanField(default=False)
    MANAGE: bool = fields.BooleanField(default=False)
    ADMIN: bool = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return f"""
            ID: {self.id},
            READ: {self.READ},
            WRITE: {self.WRITE},
            REPORT: {self.REPORT},
            MANAGE: {self.MANAGE},
            ADMIN: {self.ADMIN}
        """


class Membership(Model, CMDMixin):
    """
    Membership

    Creates a connection between an user and a company together with an ACL.
    """

    id: uuid = fields.UUIDField(primary_key=True)
    organization: Organization = fields.ForeignKeyField("models.Organization")
    user: User = fields.ForeignKeyField("models.User")
    acl: ACL = fields.ForeignKeyField("models.ACL")
    disabled: bool = fields.BooleanField(default=False)

    def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=settings.DEFAULT_TIMEZONE)
        self.save()
