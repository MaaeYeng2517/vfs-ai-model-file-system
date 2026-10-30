class ModelEngine:
    def __init__(self):
        self._artifacts = {}

    def register(self, name, version, artifact, metadata=None):
        self._artifacts.setdefault(name, {})[version] = {"artifact": artifact, "metadata": metadata or {}}

    def get(self, name, version=None):
        versions = self._artifacts.get(name, {})
        if not versions:
            raise KeyError(name)
        v = version or max(versions)
        return versions[v]

    def list_models(self):
        return list(self._artifacts)

    def list_versions(self, name):
        return sorted(self._artifacts.get(name, {}))
