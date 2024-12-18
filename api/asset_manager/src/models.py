from enum import Enum
from typing import Type
from tortoise.exceptions import ConfigurationError
from tortoise.models import Model
from tortoise import fields

class EnumField(fields.CharField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
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
                "Database value {} does not exist on Enum {}.".format(value, self._enum_type)
            )

class OrganizationType(Enum):
    HOME = 1 # Home use (Any size)
    SMALL_ORGANIZATION = 2 # 1-100
    MEDIUM_ORGANIZATION = 3 # 100 - 500
    LARGE_ORGANIZATION = 4 # 500 - 1000
    EXTRA_LARGE_ORGANIZATION = 5 # 1000 - 5000+

class CreatedAndModifiedMixin():
    created = fields.DatetimeField(null=True, auto_now_add=True)
    modified = fields.DatetimeField(null=True, auto_now=True)

class Organization(Model, CreatedAndModifiedMixin):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=128)
    type = EnumField(OrganizationType)
    users = fields.ManyToManyField('models.User',
                                   related_name='members',
                                   through="Membership",
                                   forward_key='user_id',
                                   backward_key='organization_id',
                                   null=True
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

class User(Model, CreatedAndModifiedMixin):
    id = fields.UUIDField(primary_key=True)
    name = fields.TextField()
    surname = fields.TextField()
    password = fields.CharField(max_length=128, null=True)
    organizations = fields.ManyToManyField('models.Organization',
                                           related_name='members',
                                           through='Membership',
                                           forward_key='organization_id',
                                           backward_key='user_id',
                                           null=True
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name} {self.surname}"

class Membership(Model, CreatedAndModifiedMixin):
    organization = fields.ForeignKeyField('models.Organization')
    user = fields.ForeignKeyField('models.User')
