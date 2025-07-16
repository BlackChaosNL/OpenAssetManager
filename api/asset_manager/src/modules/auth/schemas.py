from tortoise.contrib.pydantic import pydantic_model_creator

from modules.auth.models import Token

token_model = pydantic_model_creator(Token)