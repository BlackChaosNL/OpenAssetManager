from datetime import datetime
import uuid
import pytz
from tortoise import Model, fields

from modules.users.models import ACL


class Invite(Model):
    id: uuid.UUID = fields.UUIDField(primary_key=True)
    receiver: str = fields.CharField(max_length=128)
    sender: uuid.UUID = fields.UUIDField()
    org_id: uuid.UUID = fields.UUIDField()
    message: str | None = fields.TextField(null=True)
    acl: ACL = fields.ForeignKeyField("models.ACL")
    accepted: bool = fields.BooleanField(default=False)
    disabled: bool = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)

    
    async def delete(self, force: bool = False) -> None:
        if force:
            await Model.delete(self)
        else:
            self.disabled = True
            self.disabled_at = datetime.now(tz=pytz.UTC)
            await self.save()

