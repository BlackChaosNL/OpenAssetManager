import pytz
from tortoise.models import Model
from tortoise import fields
import uuid
from datetime import datetime

from mixins.CMDMixin import CMDMixin
from config import settings


class Token(Model, CMDMixin):
    """
    Token

    Creates the access tokens for the User
    """

    id: uuid = fields.UUIDField(primary_key=True)
    user: uuid = fields.ForeignKeyField("models.User")
    token_type: str = fields.CharField(max_length=128, default="Bearer")
    access_token: str = fields.TextField(null=True)
    refresh_token: str = fields.TextField(null=True)
    disabled: bool = fields.BooleanField(default=False)

    async def delete(self) -> None:
        self.disabled = True
        self.disabled_at = datetime.now(tz=pytz.UTC)
        await self.save()

