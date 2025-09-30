from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="allow"
    )

    # Supabase database URL
    database_url: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mqtt_broker: str
    mqtt_port: int
    mqtt_topic: str
    api_sensor_url: str

settings = Settings()
