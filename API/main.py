from fastapi import FastAPI
from pydantic import BaseModel
from core.retriever import IncidentRetriever
from core.reasoner import IncidentReasoner


app = FastAPI(title="AI Incident Triage Assistant")

retriever = IncidentRetriever()
reasoner = IncidentReasoner()


class IncidentRequest(BaseModel):
    query: str


@app.post("/analyze_incident")
def analyze_incident(request: IncidentRequest):
    similar = retriever.find_similar(request.query)
    result = reasoner.generate_response(request.query, similar)

    return {
        "query": request.query,
        "similar_incidents_found": len(similar),
        "analysis": result
    }
