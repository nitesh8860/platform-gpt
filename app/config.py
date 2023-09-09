from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    openai_api_key: str
    slack_token: str
    slack_bot_user: str
    sentry_dsn: str
    slack_event_token: str

    class Config:
        env_file = ".env"


settings = Settings()
