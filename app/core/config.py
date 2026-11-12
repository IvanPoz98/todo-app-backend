from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_PORT: int = 5439
    POSTGRES_DB: str = 'todo_db'

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(
        env_file='app/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()