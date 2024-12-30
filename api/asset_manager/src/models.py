from datetime import datetime
from enum import Enum
from typing import Type
import uuid
from pydantic import EmailStr
from tortoise.exceptions import ConfigurationError
from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext  # type: ignore

from src.config import settings

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EnumField(fields.CharField):
    """
    Serializes Enums to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(128, **kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Enum, instance) -> str:
        return value.value

    def to_python_value(self, value: str) -> Enum:
        try:
            return self._enum_type(value)
        except Exception:
            raise ValueError(
                "Database value {} does not exist on Enum {}.".format(
                    value, self._enum_type
                )
            )


class OrganizationType(Enum):
    """
    Represents the following:

    1. Is this a commercial entity or not?
    2. What size is it?

    All choices should be representative of the org.
    There are no seat costs.
    """

    HOME: int = 1  # Home use (Any size)
    SMALL_ORGANIZATION: int = 2  # 1-100
    MEDIUM_ORGANIZATION: int = 3  # 100 - 500
    LARGE_ORGANIZATION: int = 4  # 500 - 1000
    EXTRA_LARGE_ORGANIZATION: int = 5  # 1000 - 5000+


class CMDMixin:
    """
    Created, modified and delete mixin, these are required for every class.
    """

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)


class Organization(Model, CMDMixin):
    """
    Organization

    This class holds the organization for a household / organization
    and makes sure that we can add users.
    """

    id: uuid = fields.UUIDField(primary_key=True)
    name: str = fields.CharField(max_length=128)
    type: str = EnumField(OrganizationType)
    users: uuid = fields.ManyToManyField(
        "models.User",
        related_name="members",
        through="Membership",
        forward_key="user_id",
        backward_key="organization_id",
        null=True,
        on_delete=fields.NO_ACTION,
    )
    disabled: bool = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

    def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=settings.DEFAULT_TIMEZONE)
        self.save()


class Token(Model, CMDMixin):
    """
    Token

    Creates the access tokens for the User
    """

    id: uuid = fields.UUIDField(primary_key=True)
    user: uuid = fields.ForeignKeyField("models.User")
    token_type: str = fields.CharField(max_length=128, default="bearer")
    access_token: str = fields.CharField(max_length=128, null=True)
    refresh_token: str = fields.CharField(max_length=128, null=True)
    disabled: bool = fields.BooleanField(default=False)

    def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=settings.DEFAULT_TIMEZONE)
        self.save()


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
    tokens = fields.ForeignKeyField("models.Token")

    def __str__(self) -> str:
        return f"{self.id} - {self.name} {self.surname}"

    def set_password(self, password: str) -> None:
        secret_key = settings.SECRET_KEY
        if secret_key is None:
            return False
        self.password = crypt.hash(
            password,
            secret=secret_key,
            scheme=settings.HASHING_SCHEME,
        )
        self.save()  # Make sure to save the model in DB

    def check_against_password(self, password: str) -> bool:
        secret_key = settings.SECRET_KEY
        if secret_key is None:
            return False
        return crypt.verify(
            password,
            secret=secret_key,
            scheme=settings.HASHING_SCHEME,
        )

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
