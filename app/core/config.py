from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="allow"
    )

    database_url: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mqtt_broker: str
    mqtt_port: int
    mqtt_topic: str
    api_sensor_url: str
    vapid_public_key: str = ""
    vapid_private_key: str = ""
    vapid_claims_email: str = "mailto:admin@mitescan.com"
    temp_min_alert: float = 20.0
    temp_max_alert: float = 29.0
    humidity_min_alert: float = 45.0
    humidity_max_alert: float = 80.0

settings = Settings()
