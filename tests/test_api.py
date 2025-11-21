"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

from llm_gateway.api import create_app
from llm_gateway.api.schemas import GenerateRequest


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    # Override lifespan to avoid loading the actual model
    app.router.lifespan_context = AsyncMock()
    return TestClient(app)


@pytest.fixture
def mock_engine():
    """Mock the inference engine."""
    with patch("llm_gateway.api.routes.engine") as mock:
        mock._is_loaded = True
        mock.generate.return_value = "Generated text output"
        yield mock


def test_health_endpoint(client, mock_engine):
    """Test health check endpoint."""
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "model_name" in data


def test_generate_endpoint(client, mock_engine):
    """Test text generation endpoint."""
    request_data = {
        "prompt": "Test prompt",
        "max_length": 50,
        "temperature": 0.7,
        "stream": False,
    }
    
    response = client.post("/v1/generate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "generated_text" in data
    assert "prompt" in data
    assert "model" in data
    assert data["prompt"] == "Test prompt"


def test_generate_validation(client, mock_engine):
    """Test request validation."""
    # Missing required field
    response = client.post("/v1/generate", json={})
    assert response.status_code == 422
    
    # Invalid temperature
    response = client.post("/v1/generate", json={
        "prompt": "Test",
        "temperature": 5.0  # Too high
    })
    assert response.status_code == 422


def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    # Should return Prometheus format
    assert response.headers["content-type"].startswith("text/plain")
