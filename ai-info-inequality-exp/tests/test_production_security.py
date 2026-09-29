import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings, validate_production_config
from app.core.rate_limit import rate_limiter

client = TestClient(app)

def test_security_headers():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

def test_admin_endpoint_auth():
    orig_key = settings.ADMIN_API_KEY
    settings.ADMIN_API_KEY = "test-admin-secret-key-2026"

    try:
        # Without header -> 401
        resp_no_auth = client.get("/api/v1/admin/health")
        assert resp_no_auth.status_code == 401
        assert "Invalid administrative API key" in resp_no_auth.json()["detail"]

        # Wrong header -> 401
        resp_bad_auth = client.get("/api/v1/admin/health", headers={"X-Admin-API-Key": "wrong-key"})
        assert resp_bad_auth.status_code == 401
        assert "Invalid administrative API key" in resp_bad_auth.json()["detail"]

        # Valid header -> 200
        resp_auth = client.get("/api/v1/admin/health", headers={"X-Admin-API-Key": "test-admin-secret-key-2026"})
        assert resp_auth.status_code == 200
        assert resp_auth.json()["status"] == "HEALTHY"
    finally:
        settings.ADMIN_API_KEY = orig_key

def test_rate_limiting_enforcement():
    rate_limiter.reset()
    original_enabled = settings.RATE_LIMIT_ENABLED
    original_limit = settings.RATE_LIMIT_PER_MINUTE

    settings.RATE_LIMIT_ENABLED = True
    settings.RATE_LIMIT_PER_MINUTE = 3

    try:
        for _ in range(3):
            resp = client.post("/api/v1/session/create", json={"is_pilot": False})
            assert resp.status_code == 200

        # 4th request should exceed rate limit
        resp_exceeded = client.post("/api/v1/session/create", json={"is_pilot": False})
        assert resp_exceeded.status_code == 429
        assert "Rate limit exceeded" in resp_exceeded.json()["detail"]
    finally:
        settings.RATE_LIMIT_ENABLED = original_enabled
        settings.RATE_LIMIT_PER_MINUTE = original_limit
        rate_limiter.reset()

def test_production_config_validation():
    # Save original settings
    orig_env = settings.APP_ENV
    orig_mock = settings.USE_MOCK_LLM
    orig_key = settings.GEMINI_API_KEY
    orig_db = settings.DATABASE_URL
    orig_cors = settings.CORS_ALLOWED_ORIGINS

    try:
        # Mock mode rejected in prod
        settings.APP_ENV = "production"
        settings.USE_MOCK_LLM = True
        settings.GEMINI_API_KEY = "valid-key"
        settings.DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
        settings.CORS_ALLOWED_ORIGINS = "https://study.example.com"
        with pytest.raises(ValueError, match="USE_MOCK_LLM=True is prohibited"):
            validate_production_config()

        # Missing API key rejected
        settings.USE_MOCK_LLM = False
        settings.GEMINI_API_KEY = ""
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not configured"):
            validate_production_config()

        # SQLite rejected in prod
        settings.GEMINI_API_KEY = "valid-key"
        settings.DATABASE_URL = "sqlite:///./test.db"
        with pytest.raises(ValueError, match="SQLite DATABASE_URL is prohibited"):
            validate_production_config()

        # Wildcard CORS rejected in prod
        settings.DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
        settings.CORS_ALLOWED_ORIGINS = "*"
        with pytest.raises(ValueError, match="Insecure CORS origin '\\*' is prohibited"):
            validate_production_config()

        # Localhost CORS rejected in prod
        settings.CORS_ALLOWED_ORIGINS = "http://localhost:3000"
        with pytest.raises(ValueError, match="Insecure CORS origin 'http://localhost:3000' is prohibited"):
            validate_production_config()

        # Valid prod config passes
        settings.CORS_ALLOWED_ORIGINS = "https://study.example.com"
        validate_production_config()  # Should not raise exception
    finally:
        settings.APP_ENV = orig_env
        settings.USE_MOCK_LLM = orig_mock
        settings.GEMINI_API_KEY = orig_key
        settings.DATABASE_URL = orig_db
        settings.CORS_ALLOWED_ORIGINS = orig_cors

def test_production_error_sanitization():
    orig_env = settings.APP_ENV
    no_raise_client = TestClient(app, raise_server_exceptions=False)
    
    try:
        settings.APP_ENV = "production"
        
        @app.get("/test-500-error")
        def route_with_error():
            raise RuntimeError("Database connection string postgresql://admin:secret123@db.internal:5432 failed")

        resp = no_raise_client.get("/test-500-error")
        assert resp.status_code == 500
        assert resp.json()["detail"] == "An internal server error occurred."
        assert "secret123" not in resp.text
        assert "RuntimeError" not in resp.text
    finally:
        settings.APP_ENV = orig_env
