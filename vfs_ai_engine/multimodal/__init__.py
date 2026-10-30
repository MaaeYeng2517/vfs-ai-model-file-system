class MultimodalEngine:
    def __init__(self):
        self._assets = {}

    def store(self, id, kind, data, metadata=None):
        self._assets[id] = {"kind": kind, "data": data, "metadata": metadata or {}}

    def get(self, id):
        return self._assets[id]

    def list_by_kind(self, kind):
        return [a for a in self._assets.values() if a["kind"] == kind]
