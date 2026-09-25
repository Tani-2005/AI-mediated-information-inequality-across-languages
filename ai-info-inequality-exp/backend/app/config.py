import os
import json
from pathlib import Path
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

    class Config:
        env_file = [".env", "backend/.env"]
        extra = "ignore"

settings = Settings()

def load_experiment_config():
    with open(settings.EXPERIMENT_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

frozen_config = load_experiment_config()
