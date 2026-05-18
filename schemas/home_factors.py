"""Synthetic Home Factors property intelligence schema."""

from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class RoofMaterial(str, Enum):
    ASPHALT_SHINGLE = "asphalt_shingle"
    METAL = "metal"
    TILE = "tile"
    SLATE = "slate"
    WOOD_SHAKE = "wood_shake"
    OTHER = "other"


class ElectricalPanelType(str, Enum):
    MODERN_BREAKER = "modern_breaker"
    FEDERAL_PACIFIC = "federal_pacific"   # known fire risk
    ZINSCO = "zinsco"                      # known fire risk
    FUSE_BOX = "fuse_box"                  # outdated
    UNKNOWN = "unknown"


class PlumbingMaterial(str, Enum):
    COPPER = "copper"
    PEX = "pex"
    POLYBUTYLENE = "polybutylene"          # known failure risk
    GALVANIZED = "galvanized"              # corrosion risk
    PVC = "pvc"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class HomeFactorsRecord(BaseModel):
    """Synthetic property intelligence record."""
    property_address: str

    # Roof
    roof_material: RoofMaterial
    roof_age_years: int
    roof_replacement_recommended: bool

    # Electrical
    electrical_panel_type: ElectricalPanelType
    electrical_panel_age_years: int
    amp_service: int   # 100, 200, etc.

    # Plumbing
    plumbing_material: PlumbingMaterial
    plumbing_age_years: int
    water_intrusion_history: bool
    water_intrusion_count_5yr: int

    # Structure
    square_footage: int
    finished_basement: bool
    estimated_replacement_cost: int   # The big one for underinsurance check

    # Location risk
    fire_protection_class: int   # 1 (best) to 10 (worst)
    distance_to_fire_dept_miles: float
    distance_to_hydrant_feet: int

    # Risk factors (the agent will use these)
    notable_risk_factors: List[str] = []
