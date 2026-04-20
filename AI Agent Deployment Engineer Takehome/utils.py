import json
import os
from openai import OpenAI
from config import MODEL

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_model(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int
) -> str:
    """
    Base LLM call. All components use this.
    Returns raw string response.
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content


def parse_json_response(raw: str, fallback: dict) -> dict:
    """
    Safely parse JSON from model response.
    Returns fallback dict if parsing fails.
    """
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return json.loads(cleaned)
    except (json.JSONDecodeError, IndexError):
        return fallback