"""Prometheus metrics for observability."""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Request metrics
requests_total = Counter(
    "llm_gateway_requests_total",
    "Total number of inference requests",
    ["status"]
)

request_duration = Histogram(
    "llm_gateway_request_duration_seconds",
    "Request duration in seconds",
    ["endpoint"]
)

# Generation metrics
tokens_generated = Counter(
    "llm_gateway_tokens_generated_total",
    "Total number of tokens generated"
)

generation_duration = Histogram(
    "llm_gateway_generation_duration_seconds",
    "Token generation duration in seconds"
)

# Model metrics
model_info = Info(
    "llm_gateway_model",
    "Information about the loaded model"
)

active_requests = Gauge(
    "llm_gateway_active_requests",
    "Number of currently active requests"
)

# Batch metrics
batch_size = Histogram(
    "llm_gateway_batch_size",
    "Size of batched requests"
)


def get_metrics():
    """Return current metrics in Prometheus format."""
    return generate_latest()


def get_content_type():
    """Return Prometheus content type."""
    return CONTENT_TYPE_LATEST
