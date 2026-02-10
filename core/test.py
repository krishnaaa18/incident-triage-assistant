from core.retriever import IncidentRetriever

retriever = IncidentRetriever()

query = "Payment request failed due to timeout from external gateway"

results = retriever.find_similar(query)

print("\nTop Similar Incidents:\n")

for r in results:
    print(f"ID: {r['incident_id']}")
    print(f"Service: {r['service']}")
    print(f"Error: {r['error_type']}")
    print(f"Root Cause: {r['root_cause']}")
    print("-" * 40)
