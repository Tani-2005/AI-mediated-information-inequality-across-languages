import os
import json
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "experiment_config.json"

class Settings(BaseSettings):
    PROJECT_NAME: str = "English-Hindi AI-Mediated Information Seeking Experiment"
    APP_ENV: str = "development"
    USE_MOCK_LLM: bool = True
    IS_PILOT_MODE: bool = False
    LLM_ENABLED: bool = True
    MAX_SESSION_COUNT: int = 200
    MAX_API_CALLS_PER_SESSION: int = 30
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/backend/experiment.db"
    EXPERIMENT_CONFIG_PATH: str = str(CONFIG_PATH)
    
    # Security & Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10
    ADMIN_API_KEY: str = ""

    # Provider Hardening
    LLM_PROVIDER: str = "gemini"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-2024-08-06"

    # Gemini Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    GEMINI_MODEL: str = "gemini-3.5-flash"

    model_config = ConfigDict(
        env_file=[".env", "backend/.env"],
        extra="ignore"
    )

settings = Settings()

def validate_production_config():
    """
    Production security & configuration validation.
    Strictly prevents starting production in insecure, mock, or unencrypted states.
    """
    if settings.APP_ENV == "production":
        # 1. Reject mock mode in production
        if settings.USE_MOCK_LLM:
            raise ValueError("Production configuration error: USE_MOCK_LLM=True is prohibited in production.")

        # 2. Reject missing Gemini API key when LLM is enabled
        if settings.LLM_ENABLED and not settings.GEMINI_API_KEY:
            raise ValueError("Production configuration error: GEMINI_API_KEY is not configured.")

        # 3. Reject SQLite database in production
        if "sqlite" in settings.DATABASE_URL.lower():
            raise ValueError("Production configuration error: SQLite DATABASE_URL is prohibited in production.")

        # 4. Reject wildcard or localhost CORS origins in production
        origins = [o.strip().lower() for o in settings.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]
        for o in origins:
            if o == "*" or "localhost" in o or "127.0.0.1" in o:
                raise ValueError(f"Production configuration error: Insecure CORS origin '{o}' is prohibited in production.")

def load_experiment_config():
    with open(settings.EXPERIMENT_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

frozen_config = load_experiment_config()
