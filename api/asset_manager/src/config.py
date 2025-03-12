from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from passlib.context import CryptContext  # type: ignore
import pytz

class Settings(BaseSettings):
    PROJECT_NAME: str = "StoneEdge Asset Management System"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_SUMMARY: str = "Product API for StoneEdge."
    PROJECT_PUBLIC_URL: str = "localhost"
    SECRET_KEY: str | None = None
    PSQL_USERNAME: str = "user"
    PSQL_PASSWORD: str = "password"
    PSQL_HOSTNAME: str = "localhost"
    PSQL_PORT: int = 5432
    PSQL_DB_NAME: str = "stoneedge"
    PSQL_TEST_DB_NAME: str = "stoneedge_testing"
    ACCESS_TOKEN_EXPIRE_MIN: int = 10
    REFRESH_TOKEN_EXPIRE_MIN: int = 20
    BACKEND_CORS_ORIGINS: list = ["*"]
    CRYPT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
