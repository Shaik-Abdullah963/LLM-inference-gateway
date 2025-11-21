.PHONY: help install install-dev test lint format run clean

help:
	@echo "LLM Inference Gateway - Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code with black"
	@echo "  make run          - Run the server"
	@echo "  make clean        - Clean build artifacts"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503

format:
	black src/ tests/ examples/ benchmarks/

run:
	python -m llm_gateway.main

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
