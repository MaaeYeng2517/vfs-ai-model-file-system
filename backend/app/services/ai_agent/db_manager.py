"""Database manager for provider usage tracking."""
class ProviderDBManager:
    def __init__(self, db=None):
        self.db = db
    def log_usage(self, provider, tokens, cost):
        return {"provider": provider, "tokens": tokens, "cost": cost}
