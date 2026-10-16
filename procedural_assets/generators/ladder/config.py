from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class LadderConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial Vertical Access Ladder with Safety Cage."""
    ladder_height: float = 3.00
    ladder_width: float = 0.50
    rung_spacing: float = 0.30
    has_safety_cage: bool = True        # Protective steel hoop cage at elevated section
    cage_start_height: float = 1.60     # Elevation where protective hoops begin
    has_walkthrough_top: bool = True    # Extended flared handrails above top rung
    standoff_bracket_count: int = 3     # Pairs of wall mounting standoff brackets
    ladder_condition: str = "nominal"   # "nominal", "rusted_damaged", "missing_rung"

    name: str = "ladder"
    pivot_rule: str = "floor_center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 580
