"""Simple benchmarking script for the LLM inference gateway."""

import time
import requests
import statistics
from typing import List, Dict

BASE_URL = "http://localhost:8000/v1"


def benchmark_generation(
    prompts: List[str],
    num_runs: int = 5,
    **gen_kwargs
) -> Dict[str, float]:
    """
    Benchmark text generation performance.
    
    Args:
        prompts: List of prompts to test
        num_runs: Number of runs per prompt
        **gen_kwargs: Additional generation parameters
    
    Returns:
        Dictionary with benchmark statistics
    """
    latencies = []
    tokens_per_second = []
    
    print(f"Running benchmark with {len(prompts)} prompts, {num_runs} runs each...")
    
    for i, prompt in enumerate(prompts):
        print(f"\nPrompt {i+1}/{len(prompts)}: {prompt[:50]}...")
        
        for run in range(num_runs):
            payload = {
                "prompt": prompt,
                "stream": False,
                **gen_kwargs
            }
            
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/generate", json=payload)
            end_time = time.time()
            
            if response.status_code == 200:
                latency = end_time - start_time
                latencies.append(latency)
                
                result = response.json()
                generated_text = result.get("generated_text", "")
                # Rough token estimate (words / 0.75)
                tokens = len(generated_text.split()) / 0.75
                tps = tokens / latency if latency > 0 else 0
                tokens_per_second.append(tps)
                
                print(f"  Run {run+1}: {latency:.3f}s, ~{tps:.1f} tokens/s")
            else:
                print(f"  Run {run+1}: Error - {response.status_code}")
    
    # Calculate statistics
    stats = {
        "num_requests": len(latencies),
        "avg_latency": statistics.mean(latencies),
        "min_latency": min(latencies),
        "max_latency": max(latencies),
        "median_latency": statistics.median(latencies),
        "avg_tokens_per_sec": statistics.mean(tokens_per_second),
    }
    
    if len(latencies) > 1:
        stats["std_latency"] = statistics.stdev(latencies)
    
    return stats


def print_stats(stats: Dict[str, float]):
    """Print benchmark statistics."""
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print(f"Total Requests:        {stats['num_requests']}")
    print(f"Average Latency:       {stats['avg_latency']:.3f}s")
    print(f"Median Latency:        {stats['median_latency']:.3f}s")
    print(f"Min Latency:           {stats['min_latency']:.3f}s")
    print(f"Max Latency:           {stats['max_latency']:.3f}s")
    if 'std_latency' in stats:
        print(f"Std Dev Latency:       {stats['std_latency']:.3f}s")
    print(f"Avg Tokens/Second:     {stats['avg_tokens_per_sec']:.1f}")
    print("=" * 80)


def main():
    """Run benchmarks."""
    # Check health first
    try:
        response = requests.get(f"{BASE_URL}/health")
        health = response.json()
        print(f"Server Status: {health['status']}")
        print(f"Model: {health['model_name']}")
        print(f"Model Loaded: {health['model_loaded']}")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return
    
    # Test prompts
    prompts = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming the world by",
        "In a world where technology advances rapidly,",
        "The most important aspect of machine learning is",
        "Once upon a time in a faraway land,",
    ]
    
    # Run benchmark
    stats = benchmark_generation(
        prompts=prompts,
        num_runs=3,
        max_length=50,
        temperature=0.7,
    )
    
    # Print results
    print_stats(stats)


if __name__ == "__main__":
    main()
