from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    ACCESS_TOKEN_VK: SecretStr
    BOT_TOKEN: SecretStr
    PASSWORD_BD: SecretStr
    HOST: str
    USER_BD: SecretStr
    DATABASE: str
    PORT: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf8')


config = Settings()
