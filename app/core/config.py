from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = f"postgresql://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}:{os.getenv('postgres_port')}/{os.getenv('postgres_db')}"
    secret_key: str = "secret key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()