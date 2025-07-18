from datetime import datetime
from enum import Enum
from typing import Type
import uuid
import pytz
from tortoise.exceptions import ConfigurationError
from tortoise.models import Model
from tortoise import fields


class EnumField(fields.CharField):
    """
    Serializes Enums to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(128, **kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Enum, _) -> str:
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
    """

    HOME: str = "home"  # Home use (Any size)
    NON_PROFIT: str = "non_profit"
    SMALL_ORGANIZATION: str = "s_org"  # 1-100
    MEDIUM_ORGANIZATION: str = "m_org"  # 100 - 500
    LARGE_ORGANIZATION: str = "l_org"  # 500 - 1000
    EXTRA_LARGE_ORGANIZATION: str = "xl_org"  # 1000 - 5000+


class Organization(Model):
    """
    Organization

    This class holds the organization for a household / organization
    and makes sure that we can add users.
    """

    id: uuid.UUID = fields.UUIDField(primary_key=True)
    name: str = fields.CharField(max_length=128)
    type: str = EnumField(OrganizationType)
    street_name: str | None = fields.TextField(null=True)
    zip_code: str | None = fields.CharField(max_length=128, null=True)
    state: str | None = fields.CharField(max_length=128, null=True)
    city: str | None = fields.CharField(max_length=128, null=True)
    country: str | None = fields.CharField(max_length=128, null=True)
    users: uuid.UUID = fields.ManyToManyField(
        "models.User",
        related_name="members",
        through="Membership",
        forward_key="user_id",
        backward_key="organization_id",
        null=True,
        on_delete=fields.NO_ACTION,
    )
    disabled: bool = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

    async def delete(self, force: bool = False) -> None:
        if force:
            await Model.delete(self)
        else:
            self.disabled = True
            self.disabled_at = datetime.now(tz=pytz.UTC)
            await self.save()
