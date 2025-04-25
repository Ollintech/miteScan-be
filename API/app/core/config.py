from pydantic_settings import BaseSettings
from pydantic import Extra
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = f"postgresql://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}:{os.getenv('postgres_port')}/{os.getenv('postgres_db')}"
    algorithm: str = os.getenv("algorithm", "HS256")
    access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", 30))
    
    class Config:
        env_file = '.env'
        extra = Extra.allow

settings = Settings()