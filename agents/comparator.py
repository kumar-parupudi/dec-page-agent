import os
import json
from anthropic import Anthropic
from schemas.dec_page import ExtractedDecPage
from prompts.prompts import COMPARATOR_PROMPT
from agents import parse_json_response

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def _current_summary(dec_page: ExtractedDecPage) -> dict:
    s1 = dec_page.coverages_section1
    s2 = dec_page.coverages_section2
    return {
        "coverage_a_dwelling": s1.coverage_a_dwelling.value,
        "coverage_b_other_structures": s1.coverage_b_other_structures.value,
        "coverage_c_personal_property": s1.coverage_c_personal_property.value,
        "coverage_d_loss_of_use": s1.coverage_d_loss_of_use.value,
        "coverage_e_liability": s2.coverage_e_liability.value,
        "coverage_f_medical": s2.coverage_f_medical.value,
        "deductible_all_perils": dec_page.deductibles.all_perils.value,
        "forms_and_endorsements": dec_page.forms_and_endorsements,
        "total_premium": dec_page.premium.total_premium.value,
    }


def compare_coverage(dec_page: ExtractedDecPage, proposed: dict) -> dict:
    current = _current_summary(dec_page)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": COMPARATOR_PROMPT.format(
                current_json=json.dumps(current, indent=2),
                proposed_json=json.dumps(proposed, indent=2)
            )
        }]
    )
    return parse_json_response(response.content[0].text)
