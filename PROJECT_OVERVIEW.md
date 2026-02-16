# Incident Triage Assistant — Project Overview

**AI-powered incident triage and root cause analysis for microservices SaaS platforms.**

---

## 1. Purpose

The system analyzes production error logs or incident descriptions, finds similar historical incidents using vector similarity search, and returns structured analysis: **incident category**, **probable root cause**, **recommended actions**, and a **confidence score**. It is API-first and designed for integration into SaaS tooling.

---

## 2. Architecture

```
User → POST /analyze_incident (query)
         ↓
    IncidentRetriever (embed query → FAISS search → top-k similar incidents)
         ↓
    IncidentReasoner (Ollama/Mistral prompt → JSON analysis)
         ↓
    Hybrid confidence (retrieval + LLM)
         ↓
    Response: { query, similar_incidents_found, analysis }
```

---

## 3. Components

### 3.1 API (`API/main.py`)

| Item | Description |
|------|-------------|
| **Framework** | FastAPI |
| **Endpoint** | `POST /analyze_incident` |
| **Request** | `{ "query": "<incident description>" }` |
| **Response** | `query`, `similar_incidents_found`, `analysis` (category, probable_root_cause, recommended_actions, confidence_score) |
| **Confidence** | Average of (1) LLM confidence and (2) retrieval-based confidence from similarity distances |

### 3.2 Retrieval Pipeline

| Module | File | Role |
|--------|------|------|
| **Embedder** | `core/embeder.py` | SentenceTransformer `all-MiniLM-L6-v2` — encodes text to vectors |
| **VectorStore** | `core/vector_space.py` | FAISS L2 index — stores embeddings, nearest-neighbor search, returns `similarity_distance` |
| **IncidentRetriever** | `core/retriever.py` | Loads `data/incident.json`, embeds `service` + `error_type` + `log_summary`, exposes `find_similar(query, top_k=3)` |

### 3.3 Reasoning (`core/reasoner.py`)

| Item | Description |
|------|-------------|
| **Backend** | Ollama at `http://localhost:11434` |
| **Model** | `mistral` |
| **Prompt** | Current incident + similar historical incidents (id, service, error_type, root_cause, resolution) |
| **Output** | JSON: `incident_category`, `probable_root_cause`, `recommended_actions`, `confidence_score` |
| **Fallback** | If JSON parse fails, returns a safe default structure |

### 3.4 Data

| Item | Description |
|------|-------------|
| **Source** | `data/incident.json` |
| **Fields** | `incident_id`, `service`, `error_type`, `severity`, `log_summary`, `root_cause`, `resolution` |
| **Use** | Historical incident corpus for embedding and similarity search |

---

## 4. Dependencies (`requirements.txt`)

- **API:** fastapi, uvicorn, pydantic  
- **Embeddings:** sentence-transformers  
- **Vector search:** faiss-cpu, numpy  
- **HTTP:** requests  
- **Optional:** openai (not used in current Ollama-based flow)

---

## 5. How to Run

1. **Install:**  
   `pip install -r requirements.txt`

2. **Ollama:**  
   Ensure Ollama is running and the `mistral` model is available:  
   `ollama pull mistral` then start Ollama.

3. **Start API (from project root):**  
   `cd incident-triage-assistant`  
   `uvicorn API.main:app --reload`

4. **Call:**  
   `POST http://127.0.0.1:8000/analyze_incident`  
   Body: `{ "query": "auth-service timeout calling user-service" }`

---

## 6. Summary

- **RAG-style retrieval:** Embeddings (SentenceTransformer) + FAISS vector search over historical incidents.  
- **Local LLM:** Ollama/Mistral for structured JSON analysis.  
- **Hybrid confidence:** Combines retrieval similarity and model confidence.  
- **Structured, API-first:** Single endpoint, JSON in/out, suitable for dashboards and integrations.

---

*Document generated for the Incident Triage Assistant project.*
