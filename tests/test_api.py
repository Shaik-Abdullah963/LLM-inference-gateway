"""Tests for API endpoints."""

import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Mock torch and transformers BEFORE any imports
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()

from fastapi.testclient import TestClient


@pytest.fixture
def mock_engine():
    """Create a mock engine."""
    mock = MagicMock()
    mock._is_loaded = True
    mock.generate = Mock(return_value="Generated text output")
    return mock


@pytest.fixture
def client(mock_engine):
    """Create a test client with mocked engine."""
    # Patch the engine before importing
    with patch('llm_gateway.models.engine', mock_engine):
        with patch('llm_gateway.api.routes.engine', mock_engine):
            from llm_gateway.api import create_app
            app = create_app()
            # Skip the lifespan events
            with TestClient(app) as test_client:
                yield test_client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "model_name" in data


def test_generate_endpoint(client):
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


def test_generate_validation(client):
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
