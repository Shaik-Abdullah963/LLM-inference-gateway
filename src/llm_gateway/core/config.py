"""Configuration management for the LLM inference gateway."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ServerConfig(BaseModel):
    """Server configuration settings."""
    
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")


class ModelConfig(BaseModel):
    """Model configuration settings."""
    
    model_name: str = Field(
        default="gpt2",
        description="Hugging Face model name or path"
    )
    model_cache_dir: Optional[str] = Field(
        default="./models",
        description="Directory to cache downloaded models"
    )
    device: str = Field(default="cpu", description="Device to run inference on")
    max_length: int = Field(default=512, description="Maximum generation length")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    top_p: float = Field(default=0.9, description="Top-p sampling parameter")
    top_k: int = Field(default=50, description="Top-k sampling parameter")


class PerformanceConfig(BaseModel):
    """Performance and batching configuration."""
    
    max_batch_size: int = Field(
        default=8,
        description="Maximum batch size for inference"
    )
    batch_timeout_ms: int = Field(
        default=100,
        description="Timeout for batching requests (milliseconds)"
    )


class ObservabilityConfig(BaseModel):
    """Observability configuration (logging, metrics)."""
    
    log_level: str = Field(default="INFO", description="Logging level")
    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics"
    )
    metrics_port: int = Field(
        default=9090,
        description="Port for Prometheus metrics"
    )


class Config(BaseModel):
    """Main configuration class combining all settings."""
    
    server: ServerConfig = Field(default_factory=ServerConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            server=ServerConfig(
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8000")),
                workers=int(os.getenv("WORKERS", "1")),
            ),
            model=ModelConfig(
                model_name=os.getenv("MODEL_NAME", "gpt2"),
                model_cache_dir=os.getenv("MODEL_CACHE_DIR", "./models"),
                device=os.getenv("DEVICE", "cpu"),
                max_length=int(os.getenv("MAX_LENGTH", "512")),
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                top_p=float(os.getenv("TOP_P", "0.9")),
                top_k=int(os.getenv("TOP_K", "50")),
            ),
            performance=PerformanceConfig(
                max_batch_size=int(os.getenv("MAX_BATCH_SIZE", "8")),
                batch_timeout_ms=int(os.getenv("BATCH_TIMEOUT_MS", "100")),
            ),
            observability=ObservabilityConfig(
                log_level=os.getenv("LOG_LEVEL", "INFO"),
                metrics_enabled=os.getenv("METRICS_ENABLED", "true").lower() == "true",
                metrics_port=int(os.getenv("METRICS_PORT", "9090")),
            ),
        )


# Global configuration instance
config = Config.from_env()
