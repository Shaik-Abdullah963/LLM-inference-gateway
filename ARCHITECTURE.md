# Architecture Overview

## LLM Inference Gateway - Phase 1 (Foundation)

This document describes the architecture of the LLM Inference Gateway in its initial foundational phase.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│  (HTTP Clients, curl, Python requests, Browser, etc.)      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                    │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │  /v1/health  │ /v1/generate │     /v1/metrics      │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
│  • Request validation (Pydantic)                            │
│  • CORS handling                                            │
│  • Error handling                                           │
│  • OpenAPI documentation                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Inference Engine Layer                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │          InferenceEngine (engine.py)                │    │
│  │  • Model loading & caching                          │    │
│  │  • Text generation (standard & streaming)          │    │
│  │  • CPU optimization                                 │    │
│  │  • Token counting & metrics                        │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Hugging Face Transformers                       │
│  • Model: AutoModelForCausalLM                              │
│  • Tokenizer: AutoTokenizer                                 │
│  • Streaming: TextIteratorStreamer                          │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Layer (`src/llm_gateway/api/`)

**Purpose**: HTTP interface for client interactions

**Components**:
- `app.py`: FastAPI application factory and lifespan management
- `routes.py`: API endpoint implementations
- `schemas.py`: Pydantic request/response models

**Endpoints**:
- `GET /v1/health`: Health check and model status
- `POST /v1/generate`: Text generation (streaming & non-streaming)
- `GET /v1/metrics`: Prometheus metrics
- `GET /docs`: Swagger UI documentation
- `GET /redoc`: ReDoc documentation

**Features**:
- Async request handling
- CORS middleware
- Request validation
- Structured error responses
- Streaming responses via Server-Sent Events

### 2. Core Layer (`src/llm_gateway/core/`)

**Purpose**: Configuration management and core utilities

**Components**:
- `config.py`: Environment-based configuration using Pydantic

**Configuration Categories**:
- `ServerConfig`: Host, port, workers
- `ModelConfig`: Model selection, inference parameters
- `PerformanceConfig`: Batching settings (future)
- `ObservabilityConfig`: Logging, metrics

### 3. Models Layer (`src/llm_gateway/models/`)

**Purpose**: Model inference and generation

**Components**:
- `engine.py`: InferenceEngine class for model operations

**Capabilities**:
- Model loading with caching
- Standard text generation
- Streaming text generation
- CPU-optimized inference
- Token counting
- Exception handling in threaded generation

**Key Methods**:
- `load_model()`: Initialize model and tokenizer
- `generate()`: Synchronous text generation
- `generate_stream()`: Asynchronous streaming generation
- `unload_model()`: Free memory

### 4. Utils Layer (`src/llm_gateway/utils/`)

**Purpose**: Cross-cutting concerns (logging, metrics)

**Components**:
- `logger.py`: Structured JSON logging with structlog
- `metrics.py`: Prometheus metrics definitions

**Metrics Tracked**:
- Request counts (total, by status)
- Request duration
- Tokens generated
- Generation duration
- Active requests
- Model information

### 5. Main Entry Point (`src/llm_gateway/main.py`)

**Purpose**: Server startup and initialization

**Features**:
- Uvicorn server configuration
- Graceful shutdown handling
- Environment-based configuration loading

## Data Flow

### Standard Generation Request

```
1. Client → POST /v1/generate
   {
     "prompt": "Once upon a time",
     "max_length": 100,
     "temperature": 0.7
   }

2. API Layer → Validate request (Pydantic)
3. API Layer → Call engine.generate()
4. Inference Engine → Tokenize prompt
5. Inference Engine → Model.generate() with PyTorch
6. Inference Engine → Decode output tokens
7. Inference Engine → Update metrics
8. API Layer → Return JSON response
   {
     "generated_text": "Once upon a time...",
     "prompt": "Once upon a time",
     "model": "gpt2"
   }
```

### Streaming Generation Request

```
1. Client → POST /v1/generate (stream: true)

2. API Layer → Validate request
3. API Layer → Call engine.generate_stream()
4. Inference Engine → Start generation thread
5. Inference Engine → Stream tokens via TextIteratorStreamer
6. API Layer → Yield chunks as Server-Sent Events
7. Client → Receives tokens in real-time
8. Inference Engine → Complete & update metrics
```

## Configuration

Configuration is loaded from environment variables with defaults:

```bash
# Server
HOST=0.0.0.0
PORT=8000

# Model
MODEL_NAME=gpt2
DEVICE=cpu
MAX_LENGTH=512
TEMPERATURE=0.7

# Observability
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

## Deployment Options

### 1. Local Development
```bash
python -m llm_gateway.main
```

### 2. Docker
```bash
docker build -t llm-gateway .
docker run -p 8000:8000 llm-gateway
```

### 3. Docker Compose
```bash
docker-compose up
```

## Observability

### Logging
- Structured JSON logs via structlog
- ISO timestamp format
- Contextual information (request ID, model, etc.)
- Log levels: DEBUG, INFO, WARNING, ERROR

### Metrics (Prometheus)
- `llm_gateway_requests_total{status}`: Request counter
- `llm_gateway_request_duration_seconds{endpoint}`: Request latency
- `llm_gateway_tokens_generated_total`: Token counter
- `llm_gateway_generation_duration_seconds`: Generation time
- `llm_gateway_active_requests`: Active request gauge
- `llm_gateway_model_info`: Model metadata

## Testing

### Test Structure
```
tests/
├── test_config.py    # Configuration tests
└── test_api.py       # API endpoint tests
```

### Test Coverage
- Configuration loading and validation
- API endpoint functionality
- Request validation
- Error handling
- Metrics endpoint

### Running Tests
```bash
pytest tests/ -v
```

## Security Considerations

### Current Implementation
- Input validation via Pydantic
- CORS protection
- No authentication (suitable for internal/trusted networks)
- No rate limiting (suitable for development)

### Future Enhancements
- API key authentication
- Rate limiting
- Request size limits
- Model access controls

## Performance Characteristics

### Phase 1 (Current)
- **Target**: CPU-based inference for small models
- **Latency**: Depends on model size and hardware
- **Throughput**: Single request at a time
- **Memory**: Model loaded in RAM

### Future Phases
- **Phase 2**: Request batching for improved throughput
- **Phase 3**: KV-cache reuse for faster generation
- **Phase 4**: Hot caching for repeated prompts
- **Phase 5**: GPU support and optimization

## Dependencies

### Core
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- Transformers: Model inference
- PyTorch: Deep learning framework

### Observability
- structlog: Structured logging
- prometheus-client: Metrics

### Utilities
- python-dotenv: Environment management
- aiofiles: Async file operations

## Extension Points

The architecture is designed for evolution:

1. **Model Support**: Easy to add new model types
2. **Batching**: Infrastructure ready for batch processing
3. **Caching**: Metrics in place for cache hit/miss tracking
4. **Load Balancing**: Stateless design enables horizontal scaling
5. **Custom Endpoints**: Router pattern allows easy extension

## Limitations (Phase 1)

- Single model loaded at a time
- No request batching
- No KV-cache reuse
- CPU-only optimization
- No authentication/authorization
- No rate limiting
- Limited error recovery

These limitations are intentional for Phase 1 and will be addressed in future iterations.
