from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.users.models import User

user_model = pydantic_model_creator(User, exclude=["password"])

class register_model(BaseModel):
    email: EmailStr
    username: str
    name: str
    surname: str
    password: str
    validate_password: str


class update_user_model(BaseModel):
    email: EmailStr | None
    name: str | None
    surname: str | None
    old_password: str | None
    password: str | None
    validate_password: str | None

