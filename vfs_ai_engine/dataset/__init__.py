class DatasetEngine:
    def __init__(self):
        self._datasets = {}

    def create(self, name):
        self._datasets[name] = {"versions": {}}

    def add_version(self, name, version, data, schema=None):
        self._datasets[name]["versions"][version] = {"data": data, "schema": schema}

    def get(self, name, version=None):
        ds = self._datasets[name]
        versions = ds["versions"]
        v = version or max(versions)
        return versions[v]

    def list_datasets(self):
        return list(self._datasets)

    def list_versions(self, name):
        return sorted(self._datasets[name]["versions"])
