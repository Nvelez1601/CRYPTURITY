"""FastAPI application entry-point."""
from __future__ import annotations

from fastapi import FastAPI

from app.config.logger import configure_logging
from app.config.settings import get_settings
from app.components.wallet_checker.routes.wallet_routes import router as wallet_router
from app.middlewares.logging import LoggingMiddleware


def create_app() -> FastAPI:
    """Instantiate the FastAPI application with routes and middleware."""

    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="API para verificar wallets contra un dataset consolidado de riesgo.",
    )

    # Middlewares
    app.add_middleware(LoggingMiddleware)

    # Routers
    app.include_router(wallet_router, prefix=settings.api_prefix)

    return app


app = create_app()
