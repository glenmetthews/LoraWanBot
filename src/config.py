from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DataBaseConfig(BaseSettings):
    db_uri: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class LoraApiConfig(BaseSettings):

    api_uri: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
