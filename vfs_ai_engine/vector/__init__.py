import math

class VectorEngine:
    def __init__(self):
        self._indexes = {}

    def create_index(self, name, dim):
        self._indexes[name] = {"dim": dim, "vectors": {}}

    def upsert(self, index, id, vector, metadata=None):
        self._indexes[index]["vectors"][id] = {"vector": list(vector), "metadata": metadata or {}}

    def _cosine(self, a, b):
        dot = sum(x*y for x, y in zip(a, b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        return dot / (na*nb) if na and nb else 0.0

    def search(self, index, query, top_k=5):
        items = self._indexes[index]["vectors"]
        scored = sorted(items.items(), key=lambda kv: self._cosine(kv[1]["vector"], query), reverse=True)
        return scored[:top_k]

    def delete(self, index, id):
        self._indexes[index]["vectors"].pop(id, None)
