from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    ACCESS_TOKEN_VK: SecretStr
    BOT_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf8')


config = Settings()
