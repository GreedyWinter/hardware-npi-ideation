from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional local convenience
    load_dotenv = None


class GeminiClient:
    """Small optional Gemini adapter.

    The app remains demoable without an API key. When GEMINI_API_KEY is set,
    this client uses the Gemini API for selected generation tasks.
    """

    def __init__(self) -> None:
        if load_dotenv is not None:
            load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def generate_lines(self, prompt: str, max_lines: int = 5) -> list[str]:
        if not self.enabled:
            return []
        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(model=self.model_name, contents=prompt)
            text = getattr(response, "text", "") or ""
        except Exception:
            return []

        lines = []
        for raw in text.splitlines():
            line = raw.strip().lstrip("-*0123456789. ").strip()
            if line:
                lines.append(line)
            if len(lines) >= max_lines:
                break
        return lines
