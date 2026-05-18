"""Shared helpers."""
import json
import re


def parse_json_response(text: str) -> dict:
    """Parse JSON from Claude's response, handling markdown code fences if present."""
    # Strip markdown fences if Claude wrapped the JSON
    text = re.sub(r"^```(?:json)?\n", "", text.strip())
    text = re.sub(r"\n```$", "", text)
    return json.loads(text)
