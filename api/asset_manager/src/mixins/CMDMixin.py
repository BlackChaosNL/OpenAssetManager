from tortoise import fields

class CMDMixin():
    """
    Created, modified and delete mixin, these are required for every class.
    """

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    disabled_at = fields.DatetimeField(null=True)

