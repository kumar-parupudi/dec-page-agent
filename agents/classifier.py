import os
from anthropic import Anthropic
from schemas.dec_page import ClassificationResult
from prompts.prompts import CLASSIFIER_PROMPT
from agents import parse_json_response

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def classify_document(document_text: str) -> ClassificationResult:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": CLASSIFIER_PROMPT.format(document_text=document_text)
        }]
    )

    raw = response.content[0].text
    parsed = parse_json_response(raw)
    return ClassificationResult(**parsed)
