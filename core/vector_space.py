import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.records = []

    def add(self, embeddings, records):
        self.index.add(np.array(embeddings).astype("float32"))
        self.records.extend(records)

    def search(self, query_embedding, top_k=3):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            top_k
        )
        return [self.records[i] for i in indices[0]]
