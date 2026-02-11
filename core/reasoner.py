import requests
import json
from typing import List


class IncidentReasoner:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "mistral"

    def build_prompt(self, query: str, similar_incidents: List[dict]) -> str:
        context = "\n\n".join([
            f"Incident ID: {i['incident_id']}\n"
            f"Service: {i['service']}\n"
            f"Error: {i['error_type']}\n"
            f"Root Cause: {i['root_cause']}\n"
            f"Resolution: {i['resolution']}"
            for i in similar_incidents
        ])

        return f"""
You are an AI incident triage assistant for a microservices SaaS platform.

Current Incident:
{query}

Similar Historical Incidents:
{context}

Respond ONLY in valid JSON format:

{{
  "incident_category": "",
  "probable_root_cause": "",
  "recommended_actions": [],
  "confidence_score": 0.0
}}

Do not include explanations outside JSON.
"""

    def generate_response(self, query: str, similar_incidents: List[dict]):
        prompt = self.build_prompt(query, similar_incidents)

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        result_text = response.json().get("response", "").strip()

        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {
                "incident_category": "Unknown",
                "probable_root_cause": result_text,
                "recommended_actions": [],
                "confidence_score": 0.5
            }
