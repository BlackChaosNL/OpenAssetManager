from tortoise.contrib.pydantic import pydantic_model_creator

from modules.users.models import User

user_model = pydantic_model_creator(User, exclude=["password"])
