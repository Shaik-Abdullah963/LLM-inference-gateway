#!/usr/bin/env python3
"""Main entry point for the LLM Inference Gateway server."""

import sys
import uvicorn

from llm_gateway.core.config import config
from llm_gateway.utils import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def main():
    """Run the LLM Inference Gateway server."""
    logger.info(
        "Starting LLM Inference Gateway",
        host=config.server.host,
        port=config.server.port,
        model=config.model.model_name,
    )
    
    try:
        uvicorn.run(
            "llm_gateway.api.app:app",
            host=config.server.host,
            port=config.server.port,
            workers=config.server.workers,
            log_level=config.observability.log_level.lower(),
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
