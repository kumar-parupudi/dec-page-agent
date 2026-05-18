import re
from schemas.dec_page import ExtractedDecPage
from schemas.home_factors import HomeFactorsRecord


def _parse_dollar(value: str | None) -> int:
    if not value:
        return 0
    return int(re.sub(r"[^\d]", "", value))


def generate_quote(
    dec_page: ExtractedDecPage,
    risk_profile: dict,
    home_factors: HomeFactorsRecord | None,
) -> dict:
    current_a = _parse_dollar(dec_page.coverages_section1.coverage_a_dwelling.value)
    replacement_cost = home_factors.estimated_replacement_cost if home_factors else current_a

    proposed_a = max(current_a, replacement_cost)
    proposed_b = round(proposed_a * 0.10)
    proposed_c = round(proposed_a * 0.50)
    proposed_d = round(proposed_a * 0.20)

    # Bump liability to $500K (standard recommendation)
    proposed_e = 500_000

    # Carry over existing endorsements, add water backup if warranted
    endorsements = list(dec_page.forms_and_endorsements)
    has_water_backup = any("water backup" in e.lower() for e in endorsements)
    needs_water_backup = home_factors and (
        home_factors.finished_basement or home_factors.water_intrusion_history
    )
    if needs_water_backup and not has_water_backup:
        endorsements.append("HO-04-55 Water Backup and Sump Overflow — INCLUDED")

    # Simple premium estimate: ~0.27% of Coverage A + risk surcharges
    surcharge = 0
    if home_factors:
        if home_factors.electrical_panel_type.value in ("federal_pacific", "zinsco"):
            surcharge += 200
        if home_factors.plumbing_material.value == "polybutylene":
            surcharge += 150
        if home_factors.roof_replacement_recommended:
            surcharge += 100
    if needs_water_backup and not has_water_backup:
        surcharge += 85  # water backup endorsement cost

    proposed_premium = round(proposed_a * 0.0027 + surcharge)

    current_premium = _parse_dollar(dec_page.premium.total_premium.value)

    return {
        "coverage_a_dwelling": f"${proposed_a:,}",
        "coverage_b_other_structures": f"${proposed_b:,}",
        "coverage_c_personal_property": f"${proposed_c:,}",
        "coverage_d_loss_of_use": f"${proposed_d:,}",
        "coverage_e_liability": f"${proposed_e:,} Each Occurrence",
        "coverage_f_medical": dec_page.coverages_section2.coverage_f_medical.value or "$1,000 Each Person",
        "deductible_all_perils": dec_page.deductibles.all_perils.value or "$1,000",
        "forms_and_endorsements": endorsements,
        "total_premium": f"${proposed_premium:,}.00",
        "current_premium_for_comparison": f"${current_premium:,}.00",
    }
