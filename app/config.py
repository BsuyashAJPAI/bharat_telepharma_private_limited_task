# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", 
    "postgresql://teleuser:telepass123@localhost:5432/telemed")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me_super_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ENV: str = os.getenv("ENV", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
