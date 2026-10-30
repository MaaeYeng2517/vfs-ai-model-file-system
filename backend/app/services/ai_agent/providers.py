"""AI provider implementations (placeholders)."""
class BaseProvider:
    name = "base"
    def call(self, prompt): return ""

class OpenAIProvider(BaseProvider):
    name = "openai"
    def call(self, prompt): return "openai response"

class AnthropicProvider(BaseProvider):
    name = "anthropic"
    def call(self, prompt): return "anthropic response"

class GeminiProvider(BaseProvider):
    name = "gemini"
    def call(self, prompt): return "gemini response"
