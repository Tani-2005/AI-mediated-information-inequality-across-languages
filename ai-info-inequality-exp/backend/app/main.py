from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings, frozen_config, validate_production_config
from app.db.session import engine, Base
from app.api.v1 import (
    session, consent, screening, language_background,
    ai_literacy, randomization, tasks, chat, telemetry,
    post_task, debrief, admin
)

# Enforce strict validation when running in production environment
if settings.APP_ENV == "production":
    validate_production_config()

# Initialize local dev database tables only if using local development SQLite
if settings.APP_ENV == "development" and "sqlite" in settings.DATABASE_URL:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=frozen_config["study_metadata"]["protocol_version"],
    description="Backend API for English-Hindi AI-Mediated Information Seeking RCT Scaffolding"
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    if settings.APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
    return response

# Production Uncaught Exception Handler
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    if settings.APP_ENV == "production":
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

# CORS setup
cors_origins = [origin.strip() for origin in settings.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
app.include_router(admin.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "status": "RUNNING",
        "study_id": frozen_config["study_metadata"]["study_id"],
        "protocol_version": frozen_config["study_metadata"]["protocol_version"],
        "mode": "DEVELOPMENT_MOCK_STUB" if settings.USE_MOCK_LLM else "PRODUCTION"
    }
