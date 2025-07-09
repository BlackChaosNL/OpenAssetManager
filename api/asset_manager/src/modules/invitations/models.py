import uuid
from tortoise import Model, fields


class Invite(Model):
    id: uuid.UUID = fields.UUIDField(primary_key=True)
    receiver: str = fields.CharField(max_length=128)
    sender: uuid.UUID = fields.UUIDField()
    org_id: uuid.UUID = fields.UUIDField()
    message: str | None = fields.TextField(null=True)
    accepted: bool = fields.BooleanField()
    disabled: bool = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)
