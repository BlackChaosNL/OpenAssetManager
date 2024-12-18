from tortoise.models import Model
from tortoise import fields

class Asset(Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=128)
