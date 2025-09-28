import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="allow")
    
    database_url: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/language_prefs")
    app_name: str = "Hausa Language Learning Preference API"
    

settings = Settings()
