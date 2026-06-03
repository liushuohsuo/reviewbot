"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from reviewbot.github.webhooks import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="ReviewBot",
        description="AI-powered code review and maintainer automation",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(webhook_router, prefix="/webhook")
    return app


app = create_app()