from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings, frozen_config
from app.db.session import engine, Base
from app.api.v1 import (
    session, consent, screening, language_background,
    ai_literacy, randomization, tasks, chat, telemetry,
    post_task, debrief
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=frozen_config["study_metadata"]["protocol_version"],
    description="Backend API for English-Hindi AI-Mediated Information Seeking RCT Scaffolding"
)

# CORS setup for frontend local SPA
cors_origins = [origin.strip() for origin in settings.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 routers
app.include_router(session.router, prefix="/api/v1")
app.include_router(consent.router, prefix="/api/v1")
app.include_router(screening.router, prefix="/api/v1")
app.include_router(language_background.router, prefix="/api/v1")
app.include_router(ai_literacy.router, prefix="/api/v1")
app.include_router(randomization.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(telemetry.router, prefix="/api/v1")
app.include_router(post_task.router, prefix="/api/v1")
app.include_router(debrief.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "status": "RUNNING",
        "study_id": frozen_config["study_metadata"]["study_id"],
        "protocol_version": frozen_config["study_metadata"]["protocol_version"],
        "mode": "DEVELOPMENT_MOCK_STUB" if settings.USE_MOCK_LLM else "PRODUCTION"
    }
