from tortoise.contrib.pydantic import pydantic_model_creator

from src.models import Organization, User

OrganizationModel = pydantic_model_creator(Organization)

UserModel = pydantic_model_creator(User)
