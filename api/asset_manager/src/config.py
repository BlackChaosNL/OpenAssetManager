
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from passlib.context import CryptContext # type: ignore
import pytz

class Settings(BaseSettings):
    PROJECT_NAME: str = "Open Asset Manager"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_SUMMARY: str = "Product API for Open Asset Manager."
    SECRET_KEY: str | None = None
    HASHING_SCHEME: str = "HS512"
    PSQL_CONNECT_STR: str | None = None
    ACCESS_TOKEN_EXPIRE_MIN: int = 30
    REFRESH_TOKEN_EXPIRE_MIN: int = 60
    DEFAULT_TIMEZONE: str = pytz.UTC._tzname
    CRYPT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
