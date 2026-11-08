"""Server-only Gemini boundary. No application route can call the provider yet."""

import httpx

from app.config import settings


class PlanningUnavailable(Exception):
    pass


class GeminiAdapter:
    def status(self):
        if not settings.gemini_key or not settings.gemini_model:
            return {"available": False, "message": "AI planning is not configured yet"}
        return {
            "available": False,
            "message": "AI planning awaits scientific review and model-call authorization",
        }

    def generate(self, prompt: str):
        # This adapter is intentionally unreachable from user planning/chat routes until
        # reviewed rules, constrained output validation, quotas and jobs are implemented.
        if not settings.ai_enabled or not settings.gemini_key or not settings.gemini_model:
            raise PlanningUnavailable("AI planning is not configured yet")
        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent",
                headers={"x-goog-api-key": settings.gemini_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json"},
                },
            )
            response.raise_for_status()
            return response.json()
