"""
Rate Limiting Middleware & Dependency for Production Security
ENGLISH_HINDI_AI_INFO_INEQUALITY_2026
"""

import time
import threading
from typing import Dict, List
from fastapi import Request, HTTPException, status
from app.config import settings

class RateLimiter:
    def __init__(self):
        self._lock = threading.Lock()
        self._requests: Dict[str, List[float]] = {}

    def check_rate_limit(self, client_ip: str, max_requests: int, window_seconds: int = 60) -> bool:
        """
        Sliding window rate limit check for a client IP address.
        Returns True if request is within rate limit, False if limit exceeded.
        """
        now = time.time()
        cutoff = now - window_seconds

        with self._lock:
            # Retrieve existing request timestamps for IP
            timestamps = self._requests.get(client_ip, [])
            # Filter timestamps within active sliding window
            valid_timestamps = [ts for ts in timestamps if ts > cutoff]

            if len(valid_timestamps) >= max_requests:
                self._requests[client_ip] = valid_timestamps
                return False

            valid_timestamps.append(now)
            self._requests[client_ip] = valid_timestamps
            return True

    def reset(self):
        """Reset rate limiter state (used in unit tests)."""
        with self._lock:
            self._requests.clear()

limiter = RateLimiter()
rate_limiter = limiter

def enforce_rate_limit(request: Request):
    """
    FastAPI dependency enforcing rate limits on public endpoints.
    Uses client IP address only. Does NOT use participant research data.
    """
    if not settings.RATE_LIMIT_ENABLED:
        return

    client_ip = request.client.host if request.client else "127.0.0.1"
    max_reqs = settings.RATE_LIMIT_PER_MINUTE

    if not limiter.check_rate_limit(client_ip, max_requests=max_reqs, window_seconds=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
