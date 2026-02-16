AI Incident Triage & Root Cause Assistant

Production-style AI backend for automated incident triage in microservices-based SaaS platforms.

Overview

This system analyzes production incident descriptions, retrieves semantically similar historical failures using FAISS vector search, and performs structured root cause reasoning using a locally deployed LLM (Mistral via Ollama).

It returns:

Incident category

Probable root cause

Recommended remediation steps

Hybrid confidence score

Processing latency

Designed as an API-first backend suitable for SaaS DevOps tooling.

Key Capabilities
Retrieval-Augmented Reasoning

Uses SentenceTransformer embeddings (all-MiniLM-L6-v2) with FAISS L2 index to retrieve top-k similar historical incidents.

Local LLM Inference

Integrates Mistral via Ollama for structured JSON reasoning without external API dependency.

Hybrid Confidence Scoring

Combines:

LLM self-reported confidence

Retrieval similarity normalization

Improves reliability compared to pure LLM reasoning.

Automated Severity Prediction

Majority-vote severity estimation from historical retrieval results.

Production-Oriented Features

FastAPI REST deployment

Structured JSON validation (Pydantic)

Health check endpoint

Latency tracking

Structured logging

Evaluation framework