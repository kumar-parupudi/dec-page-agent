import json
from dotenv import load_dotenv

load_dotenv()

from agents.classifier import classify_document
from agents.extractor import extract_dec_page
from agents.risk_analyzer import analyze_risk, load_home_factors
from agents.quote_generator import generate_quote
from agents.comparator import compare_coverage


def process_dec_page(document_text: str) -> dict:
    # Stage 1: Classify
    cls = classify_document(document_text)

    # Stage 2: Extract
    ext = extract_dec_page(document_text)

    # Stage 3: Risk analysis with home factors lookup
    prop_address = ext.property.property_address.value or ""
    home_factors = load_home_factors(prop_address)
    if home_factors:
        risk = analyze_risk(ext, home_factors)
    else:
        risk = {
            "underinsurance_flags": [],
            "coverage_gaps": [],
            "property_risk_factors": [],
            "overall_recommendation_summary": "No Home Factors data available for this property.",
        }

    # Stage 4: Generate proposed quote
    proposed = generate_quote(ext, risk, home_factors)

    # Stage 5: Compare current vs proposed
    comparison = compare_coverage(ext, proposed)

    return {
        "classification": json.loads(cls.model_dump_json()),
        "extracted_dec_page": json.loads(ext.model_dump_json()),
        "risk_profile": risk,
        "comparison": comparison,
    }


if __name__ == "__main__":
    with open("sample_data/dec_page_clean.txt") as f:
        text = f.read()

    cls = classify_document(text)
    print(f"\n=== STAGE 1: CLASSIFIER ===")
    print(f"Form: {cls.policy_form} (conf: {cls.confidence})")
    print(f"Carrier: {cls.carrier_name}")
    print(f"Reasoning: {cls.reasoning}")

    ext = extract_dec_page(text)
    print(f"\n=== STAGE 2: EXTRACTOR ===")
    print(f"Policy: {ext.policy_identifiers.policy_number.value}")
    print(f"Coverage A: {ext.coverages_section1.coverage_a_dwelling.value}")
    print(f"Premium: {ext.premium.total_premium.value}")
    print(f"Mortgagee: {ext.mortgagee.name.value if ext.mortgagee else 'N/A'}")
