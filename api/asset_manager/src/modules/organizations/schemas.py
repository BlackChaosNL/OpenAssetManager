from tortoise.contrib.pydantic import pydantic_model_creator

from modules.organizations.models import Organization

OrganizationModel = pydantic_model_creator(Organization)

