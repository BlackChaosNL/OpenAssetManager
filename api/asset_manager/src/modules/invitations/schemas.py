
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.invitations.models import Invite

invitation_model = pydantic_model_creator(Invite)

