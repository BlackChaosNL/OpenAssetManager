import pytz
from tortoise.models import Model
from tortoise import fields
import uuid
from datetime import datetime


class Token(Model):
    """
    Token

    Creates the access tokens for the User
    """

    id: uuid.UUID = fields.UUIDField(primary_key=True)
    user: uuid.UUID = fields.ForeignKeyField("models.User")
    token_type: str = fields.CharField(max_length=128, default="Bearer")
    access_token: str = fields.TextField(null=True)
    refresh_token: str = fields.TextField(null=True)
    disabled: bool = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)

    async def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=pytz.UTC)
        await self.save()
