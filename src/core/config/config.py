import json
from typing import Optional
from pydantic import EmailStr, field_validator

from src.core.config.base_config import Settings
from src.models.users import Gender
from src.core.logger.logger import logger
from src.core.config.base_config import BASE_DIR

logger.debug(f"BASE_DIR: {BASE_DIR}")

class DBConfig(Settings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: int = 1234
    POSTGRES_DB: str = "alphadb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

class JWTConfig(Settings):
    SECRET_KEY: str = "1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EMAIL_TOKEN_EXPIRE_DAYS: int = 7


class AdminConfig(Settings):
    ADMIN_PASSWORD: str = "admin"
    ADMIN_FULLNAME: str = "Admin User Ampss"
    ADMIN_AGE: int = 30
    ADMIN_GENDER: Gender = Gender.M
    ADMIN_EMAIL: str ="admin@example.com"

class RedisConfig(Settings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

admin_config = AdminConfig()
db_config = DBConfig()
jwt_config = JWTConfig()
redis_config = RedisConfig()
print(f"DBConfig: {db_config.DATABASE_URL}")