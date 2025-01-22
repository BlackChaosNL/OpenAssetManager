from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from passlib.context import CryptContext  # type: ignore
import pytz


class Settings(BaseSettings):
    PROJECT_NAME: str = "StoneEdge Asset Management System"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_SUMMARY: str = "Product API for StoneEdge."
    SECRET_KEY: str | None = None
    HASHING_SCHEME: str = "HS512"
    PSQL_CONNECT_STR: str = "postgres://user:password@localhost:5432/stoneedge"
    ACCESS_TOKEN_EXPIRE_MIN: int = 30
    REFRESH_TOKEN_EXPIRE_MIN: int = 60
    DEFAULT_TIMEZONE: str = pytz.UTC._tzname
    CRYPT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
