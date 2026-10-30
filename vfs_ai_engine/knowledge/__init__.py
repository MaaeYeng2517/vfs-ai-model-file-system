class KnowledgeEngine:
    def __init__(self):
        self._docs = {}
        self._graph = {}

    def add_document(self, id, content, metadata=None):
        self._docs[id] = {"content": content, "metadata": metadata or {}}

    def get_document(self, id):
        return self._docs[id]

    def search(self, query):
        q = query.lower()
        return [d for d in self._docs.values() if q in d["content"].lower()]

    def add_edge(self, src, dst, relation):
        self._graph.setdefault(src, []).append((dst, relation))

    def neighbors(self, node):
        return self._graph.get(node, [])
