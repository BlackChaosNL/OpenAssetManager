from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.organizations.models import Organization, OrganizationType

organization_model = pydantic_model_creator(Organization)

class register_organization(BaseModel):
    name: str
    type: OrganizationType
    street_name: str | None
    zip_code: str | None
    state: str | None
    city: str | None
    country: str | None

class update_org(BaseModel):
    name: str | None
    type: OrganizationType | None
    street_name: str | None
    zip_code: str | None
    state: str | None
    city: str | None
    country: str | None