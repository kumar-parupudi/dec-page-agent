import os
from anthropic import Anthropic
from schemas.dec_page import ExtractedDecPage
from prompts.prompts import EXTRACTOR_PROMPT
from agents import parse_json_response

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def extract_dec_page(document_text: str) -> ExtractedDecPage:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": EXTRACTOR_PROMPT.format(document_text=document_text)
        }]
    )

    raw = response.content[0].text
    parsed = parse_json_response(raw)
    return ExtractedDecPage(**parsed)
