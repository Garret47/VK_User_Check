from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    PASSWORD_BD: SecretStr
    HOST: str
    USER_BD: SecretStr
    DATABASE: str
    PORT: int
    ADMINS: list

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf8')


config = Settings()
