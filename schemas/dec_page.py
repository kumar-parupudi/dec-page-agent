"""Dec Page schemas for the Dec Page Intelligence Agent."""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class PolicyForm(str, Enum):
    HO3 = "HO-3"   # Standard Special Form (most common)
    HO5 = "HO-5"   # Comprehensive
    HO6 = "HO-6"   # Condo
    HO8 = "HO-8"   # Modified (older homes, ACV)
    UNKNOWN = "UNKNOWN"


class ExtractedField(BaseModel):
    """A single extracted field with confidence and provenance."""
    value: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    source_snippet: Optional[str] = None
    notes: Optional[str] = None


class ClassificationResult(BaseModel):
    """Output of Stage 1."""
    policy_form: PolicyForm
    carrier_name: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class PolicyholderInfo(BaseModel):
    named_insured: ExtractedField
    mailing_address: ExtractedField


class PropertyInfo(BaseModel):
    property_address: ExtractedField
    construction_type: ExtractedField
    year_built: ExtractedField
    distance_to_hydrant: ExtractedField
    distance_to_fire_dept: ExtractedField


class PolicyIdentifiers(BaseModel):
    policy_number: ExtractedField
    policy_period_inception: ExtractedField
    policy_period_expiration: ExtractedField
    policy_form: ExtractedField


class CoveragesSection1(BaseModel):
    """Property coverages."""
    coverage_a_dwelling: ExtractedField
    coverage_b_other_structures: ExtractedField
    coverage_c_personal_property: ExtractedField
    coverage_d_loss_of_use: ExtractedField


class CoveragesSection2(BaseModel):
    """Liability coverages."""
    coverage_e_liability: ExtractedField
    coverage_f_medical: ExtractedField


class Deductibles(BaseModel):
    all_perils: ExtractedField
    wind_hail: Optional[ExtractedField] = None
    hurricane: Optional[ExtractedField] = None


class Discount(BaseModel):
    name: str
    applied: bool


class MortgageeInfo(BaseModel):
    name: ExtractedField
    mailing_address: ExtractedField


class CarrierInfo(BaseModel):
    company_name: ExtractedField
    company_phone: ExtractedField
    agent_name: Optional[ExtractedField] = None
    agent_phone: Optional[ExtractedField] = None


class PremiumInfo(BaseModel):
    total_premium: ExtractedField
    additional_surcharges: Optional[ExtractedField] = None


class ExtractedDecPage(BaseModel):
    """Output of Stage 2: complete extraction from a dec page."""
    policy_form: PolicyForm
    carrier: CarrierInfo
    policyholder: PolicyholderInfo
    property: PropertyInfo
    policy_identifiers: PolicyIdentifiers
    coverages_section1: CoveragesSection1
    coverages_section2: CoveragesSection2
    deductibles: Deductibles
    discounts_applied: List[str] = []
    forms_and_endorsements: List[str] = []
    mortgagee: Optional[MortgageeInfo] = None
    premium: PremiumInfo
    extraction_notes: List[str] = []
