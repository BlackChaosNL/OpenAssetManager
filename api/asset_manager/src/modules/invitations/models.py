
import uuid
from tortoise import Model, fields

from mixins import CMDMixin
from modules.users.models import User


class Invite(Model, CMDMixin):
    id: uuid.UUID = fields.UUIDField(primary_key=True)
    receiver: str = fields.CharField(max_length=128)
    sender: str = fields.UUIDField()
    message: str | None = fields.TextField(null=True)
    accepted: bool = fields.BooleanField()
    disabled: bool = fields.BooleanField(default=False)
