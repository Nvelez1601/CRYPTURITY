"""Request logging middleware."""
from __future__ import annotations

import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.config.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log incoming requests and their processing time at INFO level."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.perf_counter()
        logger.info("Request started | %s %s", request.method, request.url.path)
        response: Response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "Request finished | %s %s | status=%s | %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
