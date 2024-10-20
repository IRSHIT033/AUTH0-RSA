import decouple
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendBaseSettings(BaseSettings):
    AUTH0_DOMAIN: str = decouple.config("AUTH0_DOMAIN")
    AUTH0_API_AUDIENCE: str = decouple.config("AUTH0_API_AUDIENCE")
    AUTH0_CLIENT_ID: str = decouple.config("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET: str = decouple.config("AUTH0_CLIENT_SECRET")
    AUTH0_ALGORITHM: str = decouple.config("AUTH0_ALGORITHM")
    AUTH0_REDIRECT_URI: str = decouple.config("AUTH0_REDIRECT_URI")
    APPLICATION_URL: str = decouple.config("APPLICATION_URL")
    AUTH0_MANAGEMENT_DOMAIN: str = decouple.config("AUTH0_MANAGEMENT_DOMAIN")
    AUTH0_MANAGEMENT_CLIENT_ID: str = decouple.config("AUTH0_MANAGEMENT_CLIENT_ID")
    AUTH0_MANAGEMENT_CLIENT_SECRET: str = decouple.config(
        "AUTH0_MANAGEMENT_CLIENT_SECRET"
    )

    IS_ALLOWED_CREDENTIALS: bool = True
    # get the list of allowed origins from the environment variable

    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    SERVER_WORKERS: int = 4
    LOG_LEVEL: str = "debug"
    SERVER_RELOAD: bool = True
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return BackendBaseSettings()


settings = get_settings()
