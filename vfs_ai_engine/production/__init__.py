class ProductionEngine:
    def __init__(self):
        self._policies = {}
        self._metrics = {}

    def set_policy(self, name, value):
        self._policies[name] = value

    def get_policy(self, name):
        return self._policies.get(name)

    def record_metric(self, name, value):
        self._metrics.setdefault(name, []).append(value)

    def get_metrics(self, name):
        return self._metrics.get(name, [])
