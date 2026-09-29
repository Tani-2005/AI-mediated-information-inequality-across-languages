"""
Authentication & Authorization Security Utilities
ENGLISH_HINDI_AI_INFO_INEQUALITY_2026
"""

from fastapi import Request, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)

def require_admin_auth(api_key: str = Security(api_key_header)):
    """
    Administrative API Key security dependency.
    Restricts administrative / data dump routes in production.
    """
    if settings.APP_ENV == "development" and not settings.ADMIN_API_KEY:
        return True # Permissive in dev if admin key not set

    if not settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative access is not configured."
        )

    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative API key."
        )

    return True
