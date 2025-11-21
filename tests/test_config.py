"""Tests for configuration management."""

import os
import pytest
from llm_gateway.core.config import Config, ServerConfig, ModelConfig


def test_server_config_defaults():
    """Test server configuration defaults."""
    config = ServerConfig()
    assert config.host == "0.0.0.0"
    assert config.port == 8000
    assert config.workers == 1


def test_model_config_defaults():
    """Test model configuration defaults."""
    config = ModelConfig()
    assert config.model_name == "gpt2"
    assert config.device == "cpu"
    assert config.max_length == 512
    assert config.temperature == 0.7
    assert config.top_p == 0.9


def test_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "8080")
    monkeypatch.setenv("MODEL_NAME", "gpt2-medium")
    monkeypatch.setenv("MAX_LENGTH", "1024")
    
    config = Config.from_env()
    
    assert config.server.host == "127.0.0.1"
    assert config.server.port == 8080
    assert config.model.model_name == "gpt2-medium"
    assert config.model.max_length == 1024


def test_config_validation():
    """Test configuration validation."""
    # This should not raise an error
    config = ModelConfig(
        model_name="test-model",
        max_length=256,
        temperature=0.5,
        top_p=0.95,
    )
    assert config.max_length == 256
    assert config.temperature == 0.5
