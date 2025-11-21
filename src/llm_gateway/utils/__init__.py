"""Utilities module initialization."""

from .logger import setup_logging, get_logger
from .metrics import (
    requests_total,
    request_duration,
    tokens_generated,
    generation_duration,
    model_info,
    active_requests,
    batch_size,
    get_metrics,
    get_content_type,
)

__all__ = [
    "setup_logging",
    "get_logger",
    "requests_total",
    "request_duration",
    "tokens_generated",
    "generation_duration",
    "model_info",
    "active_requests",
    "batch_size",
    "get_metrics",
    "get_content_type",
]
