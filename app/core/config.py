from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url = f"postgresql://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}:{os.getenv('postgres_port')}/{os.getenv('postgres_db')}?client_encoding=utf8"
    secret_key: str = os.getenv("secret_key")
    algorithm: str = os.getenv("algorithm", "HS256")
    access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", 30))
    google_maps_api_key: str = os.getenv("google_maps_api_key")

settings = Settings()