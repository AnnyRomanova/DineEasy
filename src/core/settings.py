from pydantic_settings import BaseSettings
import os


class DatabaseConfig(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    def make_url(self, driver: str) -> str:
        return (
            f"{driver}://{self.USER}:{self.PASSWORD}@{self.resolved_host}:{self.PORT}/{self.DB}"
        )

    @property
    def resolved_host(self) -> str:
        env_mode = os.getenv("ENV_MODE", "local")
        return "db" if env_mode == "docker" else self.HOST

    @property
    def asyncpg_url(self) -> str:
        return self.make_url(driver="postgresql+asyncpg")

    @property
    def postgresql_url(self) -> str:
        return self.make_url(driver="postgresql")


class Settings(BaseSettings):
    APP_NAME: str
    DB: DatabaseConfig

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
