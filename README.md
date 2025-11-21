# LLM Inference Gateway

An evolving LLM inference gateway built from the ground up. It starts with a simple, CPU-friendly foundation and will gradually grow into a high-performance inference server—with batching, KV-cache reuse, streaming responses, hot caching, observability, and real benchmarking—similar to systems like vLLM, TGI, and Triton.

## Features

### Phase 1 - Foundation (Current) ✅
- **CPU-Friendly Inference**: Optimized for CPU-based inference using Hugging Face Transformers
- **Simple Model Loading**: Easy integration with any Hugging Face model
- **RESTful API**: FastAPI-based HTTP server with OpenAPI documentation
- **Streaming Responses**: Real-time token streaming for interactive applications
- **Observability**: Structured logging and Prometheus metrics
- **Configuration Management**: Environment-based configuration with sensible defaults

### Roadmap
- **Phase 2**: Request batching and queue management
- **Phase 3**: KV-cache reuse and optimization
- **Phase 4**: Hot caching for popular prompts
- **Phase 5**: Advanced benchmarking and profiling tools
- **Phase 6**: Multi-model support and model switching

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Shaik-Abdullah963/LLM-inference-gateway.git
cd LLM-inference-gateway

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Configuration

Copy the example environment file and customize as needed:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

Key configuration options:
- `MODEL_NAME`: Hugging Face model to use (default: `gpt2`)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `DEVICE`: Device for inference - `cpu` or `cuda` (default: `cpu`)
- `MAX_LENGTH`: Maximum generation length (default: `512`)

### Running the Server

```bash
# Using the main entry point
python -m llm_gateway.main

# Or using the API module directly
python -m llm_gateway.api.app
```

The server will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

## Usage

### Health Check

```bash
curl http://localhost:8000/v1/health
```

### Text Generation

**Standard Generation:**
```bash
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Once upon a time",
    "max_length": 100,
    "temperature": 0.7
  }'
```

**Streaming Generation:**
```bash
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The future of AI is",
    "max_length": 100,
    "temperature": 0.7,
    "stream": true
  }'
```

### Python Client Example

```python
import requests

# Generate text
response = requests.post(
    "http://localhost:8000/v1/generate",
    json={
        "prompt": "Artificial intelligence will",
        "max_length": 50,
        "temperature": 0.8,
    }
)

result = response.json()
print(result["generated_text"])
```

See `examples/basic_generation.py` for more examples.

## Observability

### Metrics

Prometheus metrics are available at `http://localhost:8000/v1/metrics` (when enabled).

Key metrics:
- `llm_gateway_requests_total`: Total number of requests
- `llm_gateway_request_duration_seconds`: Request latency
- `llm_gateway_tokens_generated_total`: Total tokens generated
- `llm_gateway_generation_duration_seconds`: Generation time
- `llm_gateway_active_requests`: Currently active requests

### Logging

The gateway uses structured JSON logging for easy parsing and analysis. All logs include timestamps, log levels, and contextual information.

## Benchmarking

Run the included benchmark script to measure performance:

```bash
python benchmarks/simple_benchmark.py
```

This will test various prompts and report:
- Average, min, max, and median latency
- Tokens per second
- Request throughput

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=llm_gateway tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Architecture

```
llm_gateway/
├── api/           # FastAPI application and routes
│   ├── app.py     # Application factory and lifespan
│   ├── routes.py  # API endpoints
│   └── schemas.py # Request/response models
├── core/          # Core configuration
│   └── config.py  # Configuration management
├── models/        # Model inference engine
│   └── engine.py  # Model loading and generation
└── utils/         # Utilities
    ├── logger.py  # Structured logging
    └── metrics.py # Prometheus metrics
```

## API Endpoints

- `GET /v1/health` - Health check
- `POST /v1/generate` - Generate text (supports streaming)
- `GET /v1/metrics` - Prometheus metrics
- `GET /docs` - OpenAPI documentation (Swagger UI)
- `GET /redoc` - ReDoc documentation

## License

This project is licensed under the terms of the LICENSE file.

## Contributing

Contributions are welcome! This is an evolving project, and we're building it incrementally. Areas for contribution:
- Performance optimizations
- New features from the roadmap
- Bug fixes and improvements
- Documentation enhancements
- Additional examples and benchmarks

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Hugging Face Transformers](https://huggingface.co/transformers/) - Model inference
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [Prometheus](https://prometheus.io/) - Metrics and monitoring
