from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.auth.models import Token

token_model = pydantic_model_creator(Token)

class register_model(BaseModel):
    email: EmailStr
    username: str
    name: str
    surname: str
    password: str
    validate_password: str