# 🚀 LLM Inference Gateway (Evolving Project)

This repository contains an evolving LLM inference gateway built from the ground up.  
It begins with a simple, CPU-friendly version and will expand into a more complete inference server with features such as batching, KV-cache reuse, streaming, observability, caching layers, and performance benchmarking.

The goal is to explore how modern high-throughput LLM inference systems work behind the scenes—similar in spirit to vLLM, HuggingFace TGI, and NVIDIA Triton.

---

## 🌟 Project Vision

The project starts with a minimal implementation and grows incrementally through clear, focused steps.  
Each stage adds a new capability, allowing the system to evolve from a naive baseline into a more optimized inference-serving architecture.

This repository emphasizes **architecture, inference orchestration, and system behavior**, rather than model training or fine-tuning.

---

## 🎯 Objectives

This project aims to provide a practical understanding of key concepts behind serving LLMs at scale, including:

- request routing and model lifecycle  
- continuous batching  
- KV-cache usage and memory considerations  
- latency vs throughput trade-offs  
- observability in inference systems  
- streaming token generation  
- caching strategies  

The goal is to recreate simplified versions of the ideas used in modern inference servers.

---

## 🧠 Topics Explored Over Time

### 🔹 Inference System Design
- Continuous batching fundamentals  
- KV-cache mechanics (prefill and decode phases)  
- Token streaming using FastAPI  
- Understanding GPU/CPU inference paths  

### 🔹 Infrastructure & Performance
- Redis for hot-response caching  
- Prometheus/Grafana for metrics and dashboards  
- Structured logging and latency measurements  
- Load testing with Locust or JMeter  
- Containerization with Docker  

### 🔹 Backend Engineering
- Async request handling  
- Graceful backpressure and queueing  
- Managing global model state  
- Designing scalable inference APIs  

---

## 🛠️ Features the Project Will Eventually Include

- Centralized model loader  
- Request queue and scheduling  
- Continuous batching (stub → improved)  
- Mock KV-cache → real KV-cache  
- Streaming responses  
- Metrics export and dashboards  
- Error handling and throttling  
- Deployment patterns  

---

## 📚 Development Roadmap (Commit-by-Commit Evolution)

### 🔴 Step 0 — Brute-Force Baseline  
Naive implementation that loads the model on every request.  
Used as the performance baseline. *(Next commit)*

### 🟠 Step 1 — Centralized Model Loading  
Load the model once at startup; major latency improvements.

### 🟡 Step 2 — Request Queue  
Buffer incoming requests to avoid overload.

### 🟢 Step 3 — Simple Batching (Stub)  
Group requests together to simulate batching behavior.

### 🔵 Step 4 — Mock KV-Cache  
Demonstrate prefix reuse before implementing real tensor caching.

### 🟣 Step 5 — Observability  
Add metrics, logs, latency tracking, and request stats.

### 🟤 Step 6 — Backpressure & Stability  
Concurrency limits, retries, and queue thresholds.

### ⚫ Step 7 — Real KV-Cache (Advanced)  
Implement actual attention key/value tensor caching.

---

## 📌 Current Status

- ✔ Repository scaffold created  
- ✔ Project roadmap defined  
- ❗ No implementation added yet  
- 🔜 Next step: Brute-force baseline (Step 0)  

---

## 🌍 Real-World Inspiration

This project is inspired by the design principles found in high-performance inference systems such as:

- vLLM  
- HuggingFace TGI  
- NVIDIA Triton  
- Cloud inference runtimes used across industry  

The goal is to understand and re-create these concepts at a smaller, more approachable scale.

---

## 📎 License

MIT License
