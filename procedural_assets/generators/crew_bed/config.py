from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CrewBedConfig(BaseAssetConfig):
    """Configuration for utilitarian space station crew beds and medical cots."""
    bed_type: str = "crew_cot"          # "crew_cot", "medical_gurney", "enclosed_pod"
    width: float = 1.00                 # Mattress width in meters
    length: float = 2.05                # Mattress length in meters
    height: float = 0.65                # Bed height from floor in meters
    mattress_state: str = "made_clean"  # "made_clean", "rumpled_disheveled", "bare_foam_stained"
    has_pillow: bool = True
    has_under_drawers: bool = True      # Storage compartments underneath
    has_guardrails: bool = False        # Safety / turbulence side rails
    headrest_incline: float = 0.0       # Angle in degrees (0 to 35)
    blanket_color: str = "station_gray" # "station_gray", "medical_blue", "emergency_orange", "brown_wool"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
