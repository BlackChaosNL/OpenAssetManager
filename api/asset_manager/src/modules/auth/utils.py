from datetime import timedelta
import uuid, time
from config import settings
from joserfc import jwt  # type: ignore
from joserfc.jwk import OctKey # type: ignore

crypt = settings.CRYPT


def create_token(user_id: uuid, offset: timedelta) -> str:
    """
    Creates a JWT token
    """
    user = str(user_id)
    curr_time = int(time.time())

    return jwt.encode(
        {"alg": "HS256", "typ": "JWT"},
        {
            "iss": "",
            "sub": f"id:{user}",
            "nbf": curr_time,
            "iat": curr_time,
            "exp": int(time.time() + offset.total_seconds()),
        },
        OctKey.import_key(settings.SECRET_KEY),
    )


def decode_token(token: str):
    pass
