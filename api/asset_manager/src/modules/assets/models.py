from tortoise.models import Model
from tortoise import fields
from mixins.CMDMixin import CMDMixin

class Asset(Model, CMDMixin):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=128)
