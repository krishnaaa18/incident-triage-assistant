import json
from .embeder import Embedder
from .vector_space import VectorStore


class IncidentRetriever:
    def __init__(self, data_path="data/incident.json"):
        self.embedder = Embedder()

        with open(data_path, "r") as f:
            self.incident = json.load(f)

        texts = [
            f"{i['service']} {i['error_type']} {i['log_summary']}"
            for i in self.incident
        ]

        embeddings = self.embedder.embed(texts)
        self.vector_store = VectorStore(len(embeddings[0]))
        self.vector_store.add(embeddings, self.incident)

    def find_similar(self, query_text, top_k=3):
        query_embedding = self.embedder.embed([query_text])[0]
        return self.vector_store.search(query_embedding, top_k)
