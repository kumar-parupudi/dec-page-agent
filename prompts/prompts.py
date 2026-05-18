"""All LLM prompts for the Dec Page Intelligence Agent."""

CLASSIFIER_PROMPT = """You are an insurance document classifier specialized in homeowners declaration pages.

Given the text of a document, identify:
1. Whether this is a homeowners dec page (versus auto, life, commercial, etc.)
2. If yes, which specific policy form (HO-3, HO-5, HO-6, HO-8)
3. The carrier name if identifiable

Policy form definitions:
- HO-3: Standard Special Form (most common). Open peril dwelling, named peril contents.
- HO-5: Comprehensive. Open peril for both dwelling and contents.
- HO-6: Condo unit policy.
- HO-8: Modified policy for older/historic homes; loss settlement on actual cash value.

Respond with valid JSON matching this exact structure:
{{
  "policy_form": "HO-3" | "HO-5" | "HO-6" | "HO-8" | "UNKNOWN",
  "carrier_name": "<name or null>",
  "confidence": <float 0.0 to 1.0>,
  "reasoning": "<brief explanation>"
}}

Document text:
---
{document_text}
---

Respond with ONLY the JSON object, no other text, no markdown code fences."""


EXTRACTOR_PROMPT = """You are an insurance dec page extraction agent specialized in HO-3 homeowners policies.

Extract every field below from the provided document. For each field:
- Provide the value extracted (or null if not present)
- Provide a confidence score 0.0 to 1.0 (use 0.3 if unsure, 0.7 if confident, 0.95 if certain)
- Provide a short source_snippet showing where in the document you found it
- Add notes if anything is ambiguous

Use null for any field you cannot locate. Do not guess. Low confidence is better than fabrication.

Respond with JSON matching this EXACT structure (every field is required):

{{
  "policy_form": "HO-3",
  "carrier": {{
    "company_name": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "company_phone": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "agent_name": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "agent_phone": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "policyholder": {{
    "named_insured": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "mailing_address": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "property": {{
    "property_address": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "construction_type": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "year_built": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "distance_to_hydrant": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "distance_to_fire_dept": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "policy_identifiers": {{
    "policy_number": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "policy_period_inception": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "policy_period_expiration": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "policy_form": {{"value": "HO-3", "confidence": 0.95, "source_snippet": "...", "notes": null}}
  }},
  "coverages_section1": {{
    "coverage_a_dwelling": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "coverage_b_other_structures": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "coverage_c_personal_property": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "coverage_d_loss_of_use": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "coverages_section2": {{
    "coverage_e_liability": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "coverage_f_medical": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "deductibles": {{
    "all_perils": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "wind_hail": null,
    "hurricane": null
  }},
  "discounts_applied": ["list", "of", "discount names"],
  "forms_and_endorsements": ["list", "of", "form codes"],
  "mortgagee": {{
    "name": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "mailing_address": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}}
  }},
  "premium": {{
    "total_premium": {{"value": "...", "confidence": 0.9, "source_snippet": "...", "notes": null}},
    "additional_surcharges": null
  }},
  "extraction_notes": ["any general notes about extraction quality or ambiguities"]
}}

Document text:
---
{document_text}
---

Respond with ONLY the JSON object, no other text, no markdown code fences."""


RISK_ANALYZER_PROMPT = """You are a homeowners insurance risk analyzer.

You have:
1. An extracted dec page (the customer's current coverage)
2. A Home Factors property intelligence record (property attributes beyond the dec page)

Your job is to identify:
1. **Underinsurance signals**: Is Coverage A adequate vs estimated replacement cost? Are other coverages proportional?
2. **Coverage gaps**: What endorsements or coverages are missing that this property's risk profile warrants?
3. **Property risk factors**: What does the Home Factors data reveal that affects insurability and pricing?
4. **Recommendations**: What changes should the proposed quote include?

Specifically check for:
- Coverage A vs estimated_replacement_cost (flag if A is more than 10% below replacement cost)
- Missing umbrella when Coverage E is at standard $300K
- Missing water backup when finished_basement is true or water_intrusion_history is true
- Missing service line coverage when applicable
- Missing scheduled personal property when Coverage C exceeds $200K (suggests valuable items)
- Federal Pacific or Zinsco electrical panel (insurability red flag)
- Polybutylene plumbing (insurability red flag)
- Roof past useful life (typically 20-25 years for asphalt)

Respond with valid JSON:
{{
  "underinsurance_flags": [
    {{
      "type": "<flag type>",
      "current_value": "<current>",
      "recommended_value": "<recommended>",
      "rationale": "<explanation>",
      "severity": "high" | "medium" | "low"
    }}
  ],
  "coverage_gaps": [
    {{
      "missing_coverage": "<name>",
      "rationale": "<why this property needs it>",
      "estimated_limit_recommendation": "<value>"
    }}
  ],
  "property_risk_factors": [
    {{
      "factor": "<description>",
      "underwriting_impact": "<how this affects insurability or pricing>"
    }}
  ],
  "overall_recommendation_summary": "<2-3 sentence summary>"
}}

CURRENT DEC PAGE EXTRACTION:
{dec_page_json}

HOME FACTORS PROPERTY INTELLIGENCE:
{home_factors_json}

Respond with ONLY the JSON object, no other text, no markdown code fences."""


COMPARATOR_PROMPT = """You are a homeowners insurance comparison and packaging agent.

You have:
1. The customer's CURRENT coverage (extracted dec page)
2. The PROPOSED coverage (generated quote)

Generate a side-by-side comparison and an agent-ready narrative.

For each coverage line, classify the change as:
- IMPROVED (proposed is better for the customer)
- REDUCED (proposed is less than current, requires justification)
- UNCHANGED
- GAP_CLOSED (current was missing this, proposed adds it)
- NEW_COVERAGE (a coverage the customer didn't previously consider)

Then generate:
1. Side-by-side data in structured format
2. An agent talking script (3-5 sentences, conversational, customer-friendly)
3. A customer summary (1-2 sentences, plain language)

Respond with valid JSON:
{{
  "comparison_rows": [
    {{
      "coverage_element": "<name>",
      "current": "<value or 'Not included'>",
      "proposed": "<value>",
      "signal": "IMPROVED" | "REDUCED" | "UNCHANGED" | "GAP_CLOSED" | "NEW_COVERAGE",
      "explanation": "<one sentence>"
    }}
  ],
  "premium_comparison": {{
    "current_annual": "<amount>",
    "proposed_annual": "<amount>",
    "difference": "<+/- amount>",
    "monthly_difference": "<+/- amount>"
  }},
  "agent_talking_script": "<3-5 sentences for the agent to use with the customer>",
  "customer_summary": "<1-2 sentences in plain language for the customer>",
  "key_value_props": [
    "<top 3-5 value propositions of switching to the proposed coverage>"
  ]
}}

CURRENT COVERAGE:
{current_json}

PROPOSED COVERAGE:
{proposed_json}

Respond with ONLY the JSON object, no other text, no markdown code fences."""
