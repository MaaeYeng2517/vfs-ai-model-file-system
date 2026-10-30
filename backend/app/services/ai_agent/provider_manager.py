"""Provider manager for AI agent APIs."""
class ProviderManager:
    def __init__(self, providers=None, budget=0.0):
        self.providers = providers or []
        self.budget = budget
        self.spent = 0.0
        self.calls = 0

    def select(self):
        return self.providers[0] if self.providers else None

    def record(self, tokens, cost):
        self.calls += 1
        self.spent += cost
