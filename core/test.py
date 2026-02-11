from core.retriever import IncidentRetriever
from core.reasoner import IncidentReasoner

retriever = IncidentRetriever()
reasoner = IncidentReasoner()

query = "Payment request failed due to timeout from external gateway"

similar = retriever.find_similar(query)

print("\nSimilar Incidents Retrieved:\n")
for r in similar:
    print(f"{r['incident_id']} - {r['error_type']}")

print("\nAI Generated Root Cause Analysis:\n")

result = reasoner.generate_response(query, similar)

print(result)
