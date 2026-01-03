import os
import time
from groq import Groq


class LLMClient:
    """
    Lazy Groq client with retry + exponential backoff.
    Does NOT crash if API key is missing.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant", max_retries: int = 3):
        self.model = model
        self.max_retries = max_retries
        self._client = None

    def _get_client(self):
        if self._client is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise RuntimeError("GROQ_API_KEY not set")
            self._client = Groq(api_key=api_key)
        return self._client

    def reason(self, prompt: str) -> str:
        client = self._get_client()

        attempt = 0
        backoff = 1  # seconds
        print(client)

        while attempt < self.max_retries:
            try:
                print("we are here")
                print(self.model)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a careful business decision analyst. "
                                "Return only valid JSON as instructed."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                print(response)

                return response.choices[0].message.content

            except Exception as e:
                print("[ERROR] Groq call failed:", repr(e))
                attempt += 1

                if attempt >= self.max_retries:
                    raise RuntimeError(
                        f"LLM failed after {self.max_retries} attempts"
                    ) from e

                time.sleep(backoff)
                backoff *= 2

