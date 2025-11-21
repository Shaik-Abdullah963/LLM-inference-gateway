from setuptools import setup, find_packages

setup(
    name="llm-inference-gateway",
    version="0.1.0",
    description="An evolving LLM inference gateway built from the ground up",
    author="LLM Gateway Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "transformers>=4.35.2",
        "torch>=2.1.1",
        "accelerate>=0.25.0",
        "sentencepiece>=0.1.99",
        "protobuf>=4.25.1",
        "prometheus-client>=0.19.0",
        "structlog>=23.2.0",
        "python-dotenv>=1.0.0",
        "aiofiles>=23.2.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "httpx>=0.25.2",
            "black>=23.11.0",
            "flake8>=6.1.0",
        ],
    },
)
