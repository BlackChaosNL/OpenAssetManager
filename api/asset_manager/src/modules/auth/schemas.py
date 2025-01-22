from tortoise.contrib.pydantic import pydantic_model_creator

from modules.auth.models import Token

TokenModel = pydantic_model_creator(Token)
