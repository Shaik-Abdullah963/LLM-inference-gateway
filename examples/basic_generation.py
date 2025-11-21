"""Example: Basic text generation using the inference gateway."""

import requests
import json

# Gateway URL
BASE_URL = "http://localhost:8000/v1"


def check_health():
    """Check if the server is healthy."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", json.dumps(response.json(), indent=2))
    return response.json()


def generate_text(prompt, stream=False):
    """Generate text from a prompt."""
    payload = {
        "prompt": prompt,
        "max_length": 100,
        "temperature": 0.7,
        "stream": stream
    }
    
    if stream:
        # Streaming response
        print(f"\nPrompt: {prompt}")
        print("Generated (streaming):", end=" ", flush=True)
        
        response = requests.post(
            f"{BASE_URL}/generate",
            json=payload,
            stream=True
        )
        
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
        print("\n")
    else:
        # Standard response
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        result = response.json()
        print(f"\nPrompt: {prompt}")
        print(f"Generated: {result['generated_text']}\n")
        return result


def main():
    """Run example generations."""
    print("=" * 80)
    print("LLM Inference Gateway - Basic Example")
    print("=" * 80)
    
    # Check health
    health = check_health()
    if not health.get("model_loaded"):
        print("Error: Model not loaded!")
        return
    
    print("\n" + "=" * 80)
    print("Standard Generation")
    print("=" * 80)
    
    # Example 1: Standard generation
    generate_text("Once upon a time in a distant galaxy,")
    
    # Example 2: Another prompt
    generate_text("The future of artificial intelligence is")
    
    print("=" * 80)
    print("Streaming Generation")
    print("=" * 80)
    
    # Example 3: Streaming generation
    generate_text("In the year 2050, technology will", stream=True)
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
