import uuid, time
from config import settings
from joserfc import jwt  # type: ignore
from joserfc.jwt import OctKey  # type: ignore

crypt = settings.CRYPT


def crypt_password(password) -> str:
    """
    Creates a hash from the "Password" given, that can then be checked against the DB.
    """
    return crypt.hash(password, settings.HASHING_SCHEME)


def create_token(user_id: uuid, offset: float) -> str:
    """
    Creates a JWT token
    """
    curr_time = int(time.time())

    return jwt.encode(
        {"alg": settings.HASHING_SCHEME, "typ": "JWT"},
        {
            "iss": "",
            "sub": user_id,
            "nbf": curr_time,
            "iat": curr_time,
            "exp": int(curr_time + offset),
        },
        OctKey.import_key(settings.SECRET_KEY),
    )


def decode_token(token: str):
    pass
