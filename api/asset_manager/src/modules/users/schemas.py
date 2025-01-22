from tortoise.contrib.pydantic import pydantic_model_creator

from modules.users.models import User

UserModel = pydantic_model_creator(User)
