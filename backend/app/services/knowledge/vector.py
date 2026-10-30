"""In-memory vector search (Phase 3 placeholder)."""
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


class VectorStore:
    def __init__(self):
        self.items = []

    def add(self, vec, meta):
        self.items.append((vec, meta))

    def search(self, q, k=5):
        ranked = sorted(self.items, key=lambda x: cosine(q, x[0]), reverse=True)
        return [m for _, m in ranked[:k]]
