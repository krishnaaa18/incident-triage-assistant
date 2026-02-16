# API/main.py

import time
import logging
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List
from core.retriever import IncidentRetriever
from core.reasoner import IncidentReasoner

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    filename="incident_system.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------------------------------------
# FastAPI Initialization
# --------------------------------------------------

app = FastAPI(title="AI Incident Triage Assistant")

retriever = IncidentRetriever()
reasoner = IncidentReasoner()

# --------------------------------------------------
# Request & Response Models
# --------------------------------------------------

class IncidentRequest(BaseModel):
    query: str


class LLMAnalysis(BaseModel):
    incident_category: str
    probable_root_cause: str
    recommended_actions: List[str]
    confidence_score: float


# --------------------------------------------------
# Utility: Ollama Health Check
# --------------------------------------------------

def check_ollama():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=3
        )
        return "mistral" in result.stdout
    except Exception:
        return False


# --------------------------------------------------
# Health Endpoint
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "api_status": "running",
        "ollama_available": check_ollama(),
        "vector_index_loaded": True,
        "model": "mistral"
    }


# --------------------------------------------------
# Analyze Incident Endpoint
# --------------------------------------------------

@app.post("/analyze_incident")
def analyze_incident(request: IncidentRequest):

    start_time = time.time()

    try:
        # 1️⃣ Retrieve similar incidents
        similar_incidents = retriever.find_similar(request.query, top_k=3)

        # 2️⃣ LLM Reasoning
        raw_analysis = reasoner.analyze(request.query, similar_incidents)

        # 3️⃣ Validate LLM JSON Structure
        try:
            validated_analysis = LLMAnalysis(**raw_analysis)
        except ValidationError:
            validated_analysis = LLMAnalysis(
                incident_category="unknown",
                probable_root_cause="Unable to determine",
                recommended_actions=["Manual investigation required"],
                confidence_score=0.0
            )

        # 4️⃣ Retrieval-Based Confidence
        if similar_incidents:
            avg_distance = sum(i["similarity_distance"] for i in similar_incidents) / len(similar_incidents)
            retrieval_confidence = max(0.0, min(1.0, 1 - avg_distance))
        else:
            retrieval_confidence = 0.0

        # 5️⃣ Hybrid Confidence
        hybrid_confidence = round(
            (validated_analysis.confidence_score + retrieval_confidence) / 2,
            3
        )

        # 6️⃣ Latency Calculation
        processing_time = round(time.time() - start_time, 3)

        # 7️⃣ Logging
        logging.info(
            f"Query='{request.query}' | "
            f"Category='{validated_analysis.incident_category}' | "
            f"HybridConfidence={hybrid_confidence} | "
            f"Latency={processing_time}s"
        )

        return {
            "query": request.query,
            "similar_incidents_found": len(similar_incidents),
            "analysis": {
                "incident_category": validated_analysis.incident_category,
                "probable_root_cause": validated_analysis.probable_root_cause,
                "recommended_actions": validated_analysis.recommended_actions,
                "confidence_score": hybrid_confidence
            },
            "processing_time_seconds": processing_time
        }

    except Exception as e:
        logging.error(f"Error processing incident: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
