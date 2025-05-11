from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        extra="allow"
    )

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mqtt_broker: str
    mqtt_port: int
    mqtt_topic: str
    api_sensor_url: str

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()
