from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("database_url")
    secret_key: str = os.getenv("secret_key")
    algorithm: str = os.getenv("algorithm", "HS256")
    access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", 30))
    google_maps_api_key: str = os.getenv("google_maps_api_key")

settings = Settings()