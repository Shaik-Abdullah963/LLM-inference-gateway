"""FastAPI application setup."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm_gateway.api.routes import router
from llm_gateway.models import engine
from llm_gateway.utils import setup_logging, get_logger
from llm_gateway.core.config import config

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting LLM Inference Gateway")
    logger.info("Loading model", model=config.model.model_name)
    
    try:
        engine.load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error("Failed to load model", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down LLM Inference Gateway")
    engine.unload_model()
    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LLM Inference Gateway",
        description=(
            "An evolving LLM inference gateway built from the ground up. "
            "CPU-friendly foundation with streaming responses and observability."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router, prefix="/v1")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "llm_gateway.api.app:app",
        host=config.server.host,
        port=config.server.port,
        reload=False,
    )
