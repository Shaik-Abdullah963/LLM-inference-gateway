"""API request and response models."""

from typing import Optional, List
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request model for text generation."""
    
    prompt: str = Field(..., description="Input text prompt")
    max_length: Optional[int] = Field(
        None,
        description="Maximum length of generated text",
        ge=1,
        le=2048
    )
    temperature: Optional[float] = Field(
        None,
        description="Sampling temperature (0.0 = deterministic)",
        ge=0.0,
        le=2.0
    )
    top_p: Optional[float] = Field(
        None,
        description="Top-p sampling parameter",
        ge=0.0,
        le=1.0
    )
    top_k: Optional[int] = Field(
        None,
        description="Top-k sampling parameter",
        ge=1
    )
    stream: bool = Field(
        False,
        description="Enable streaming response"
    )


class GenerateResponse(BaseModel):
    """Response model for text generation."""
    
    generated_text: str = Field(..., description="Generated text")
    prompt: str = Field(..., description="Original prompt")
    model: str = Field(..., description="Model used for generation")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Health status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_name: str = Field(..., description="Name of the loaded model")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
