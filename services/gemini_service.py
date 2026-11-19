import json

from google import genai
from google.genai import types

from settings import GEMINI_API_KEY, GEMINI_MODEL


class GeminiServiceError(Exception):
    pass


def _client():
    if not GEMINI_API_KEY:
        raise GeminiServiceError("Gemini API key is not configured")
    return genai.Client(api_key=GEMINI_API_KEY)


def analyze_document(content: str) -> dict:
    prompt = f"""
Role: You are a careful document analyst.
Task: Summarize and classify the supplied document.
Context: Use only the provided document content. Do not invent missing facts.
Format: Return JSON with summary, key_points, category, suggested_priority.
Category must be one of: technical, business, general.
Suggested priority must be an integer from 1 to 5.

Document content:
{content}
"""

    try:
        response = _client().models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "summary": {"type": "STRING"},
                        "key_points": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "category": {"type": "STRING", "enum": ["technical", "business", "general"]},
                        "suggested_priority": {"type": "INTEGER", "minimum": 1, "maximum": 5},
                    },
                    "required": ["summary", "key_points", "category", "suggested_priority"],
                },
            ),
        )
        text = response.text
        if not text:
            raise GeminiServiceError("Gemini returned an empty response")
        result = json.loads(text)
        return result
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError("Gemini analysis failed") from exc
