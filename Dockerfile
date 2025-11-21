FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY setup.py .

# Install the package
RUN pip install -e .

# Expose ports
EXPOSE 8000 9090

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV MODEL_NAME=gpt2
ENV DEVICE=cpu

# Run the application
CMD ["python", "-m", "llm_gateway.main"]
