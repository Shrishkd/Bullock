import httpx
from app.core.config import settings


class LLMClient:
    """
    Simple wrapper around an OpenAI-compatible chat/completions API.
    You can point this to OpenAI, Groq, local server, etc.
    """

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def chat(self, system_prompt: str, user_message: str) -> str:
        if not self.api_key:
            return "LLM API key not configured. This is a stub response."

        headers = {"Authorization": f"Bearer {self.api_key}"}
        json_data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.3,
        }
        resp = httpx.post(self.base_url, headers=headers, json=json_data, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
