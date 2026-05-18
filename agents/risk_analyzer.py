import os
import json
from anthropic import Anthropic
from schemas.dec_page import ExtractedDecPage
from schemas.home_factors import HomeFactorsRecord
from prompts.prompts import RISK_ANALYZER_PROMPT
from agents import parse_json_response

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def load_home_factors(property_address: str) -> HomeFactorsRecord | None:
    try:
        with open("sample_data/home_factors.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    addr = property_address.lower()
    for p in data["properties"]:
        candidate = p["property_address"].lower()
        if candidate in addr or addr in candidate:
            return HomeFactorsRecord(**p)
    return None


def analyze_risk(dec_page: ExtractedDecPage, home_factors: HomeFactorsRecord) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": RISK_ANALYZER_PROMPT.format(
                dec_page_json=dec_page.model_dump_json(indent=2),
                home_factors_json=home_factors.model_dump_json(indent=2)
            )
        }]
    )
    return parse_json_response(response.content[0].text)
