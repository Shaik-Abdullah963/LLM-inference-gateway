#!/bin/bash
# Quick start script for LLM Inference Gateway

set -e

echo "========================================="
echo "LLM Inference Gateway - Quick Start"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python -m llm_gateway.main"
echo ""
echo "Or simply run:"
echo "  make run"
echo ""
echo "API documentation will be available at:"
echo "  http://localhost:8000/docs"
echo ""
