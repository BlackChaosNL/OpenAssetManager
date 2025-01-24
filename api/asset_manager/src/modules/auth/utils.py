import uuid, time
from config import settings
from joserfc import jwt  # type: ignore

crypt = settings.CRYPT


def create_token(user_id: uuid, offset: float) -> str:
    """
    Creates a JWT token
    """
    curr_time = int(time.time())

    return jwt.encode(
        {"alg": settings.HASHING_SCHEME, "typ": "JWT"},
        {
            "iss": "",
            "sub": f"id:{user_id}",
            "nbf": curr_time,
            "iat": curr_time,
            "exp": int(curr_time + offset),
        },
        settings.SECRET_KEY,
    )


def decode_token(token: str):
    pass
