class RuntimeEngine:
    def __init__(self):
        self._backends = {}

    def register(self, name, backend):
        self._backends[name] = backend

    def get(self, name):
        return self._backends[name]

    def list_backends(self):
        return list(self._backends)
