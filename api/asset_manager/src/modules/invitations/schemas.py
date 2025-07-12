import uuid
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.invitations.models import Invite

invitation_model = pydantic_model_creator(Invite)

class acl_model(BaseModel):
    READ: bool
    WRITE: bool
    REPORT: bool
    MANAGE: bool
    ADMIN: bool

class send_invitation_for_org(BaseModel):
    org_id: uuid.UUID
    receiver: str
    acl: acl_model | None
    message: str | None
