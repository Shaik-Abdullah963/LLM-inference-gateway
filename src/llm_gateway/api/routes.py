"""API routes for the LLM inference gateway."""

import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from llm_gateway.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    ErrorResponse,
)
from llm_gateway.models import engine
from llm_gateway.core.config import config
from llm_gateway.utils import (
    get_logger,
    requests_total,
    request_duration,
    active_requests,
)

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=engine._is_loaded,
        model_name=config.model.model_name,
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate text from a prompt.
    
    This endpoint supports both standard and streaming responses.
    Set `stream: true` in the request body for streaming.
    """
    if request.stream:
        # Return streaming response
        async def generate_chunks():
            success = False
            try:
                active_requests.inc()
                async for chunk in engine.generate_stream(
                    prompt=request.prompt,
                    max_length=request.max_length,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k,
                ):
                    yield chunk
                success = True
            except Exception as e:
                logger.error("Streaming generation failed", error=str(e))
                yield f"\n\nError: {str(e)}"
                requests_total.labels(status="error").inc()
            finally:
                active_requests.dec()
                if success:
                    requests_total.labels(status="success").inc()
        
        return StreamingResponse(
            generate_chunks(),
            media_type="text/plain"
        )
    
    # Standard (non-streaming) generation
    start_time = time.time()
    active_requests.inc()
    
    try:
        generated_text = engine.generate(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
        )
        
        requests_total.labels(status="success").inc()
        request_duration.labels(endpoint="/generate").observe(
            time.time() - start_time
        )
        
        return GenerateResponse(
            generated_text=generated_text,
            prompt=request.prompt,
            model=config.model.model_name,
        )
        
    except Exception as e:
        logger.error("Generation failed", error=str(e))
        requests_total.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        active_requests.dec()


@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    from llm_gateway.utils import get_metrics, get_content_type
    
    return StreamingResponse(
        iter([get_metrics()]),
        media_type=get_content_type(),
    )
