# Contributing to LLM Inference Gateway

Thank you for your interest in contributing to the LLM Inference Gateway! This is an evolving project being built incrementally, and we welcome contributions of all kinds.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/LLM-inference-gateway.git
cd LLM-inference-gateway
```

2. Set up the development environment:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

3. Run tests to verify setup:
```bash
pytest
```

## Development Workflow

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure they follow the project style:
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/ --max-line-length=100
```

3. Add tests for new functionality:
```bash
# Run tests
pytest

# Check coverage
pytest --cov=llm_gateway tests/
```

4. Commit your changes:
```bash
git add .
git commit -m "Add: brief description of changes"
```

5. Push and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length is 100 characters
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes

## Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common test setup
- Mock external dependencies in unit tests

## Areas for Contribution

### High Priority
- Request batching implementation
- KV-cache reuse optimization
- Performance benchmarking tools
- Memory optimization for CPU inference

### Medium Priority
- Multi-model support
- Model hot-swapping
- Advanced caching mechanisms
- Load balancing for multiple workers

### Low Priority
- Additional model backends
- UI dashboard for monitoring
- Advanced logging features
- Integration examples

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new code
- Update API documentation if endpoints change
- Add examples for new features

## Commit Messages

Follow conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Build/config changes

Example: `feat: add request batching with configurable timeout`

## Pull Request Process

1. Ensure all tests pass
2. Update documentation as needed
3. Add entry to CHANGELOG.md (if exists)
4. Request review from maintainers
5. Address review feedback

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Ideas for improvements

Thank you for contributing to LLM Inference Gateway!
