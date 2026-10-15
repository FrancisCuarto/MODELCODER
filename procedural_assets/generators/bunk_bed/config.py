from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class BunkBedConfig(BaseAssetConfig):
    """Configuration for two-tier stacked crew bunk beds."""
    frame_style: str = "tubular_metal"       # "tubular_metal", "reinforced_bulkhead", "capsule_stacked"
    width: float = 1.05                     # Bunk width in meters
    length: float = 2.05                    # Bunk length in meters
    height: float = 2.05                    # Total height in meters
    ladder_position: str = "front_right"    # "front_right", "front_left", "side_head"
    upper_guardrail: bool = True            # Safety barrier on upper bunk
    lower_bunk_state: str = "made"          # "made", "disheveled", "bare_foam_stained"
    upper_bunk_state: str = "made"          # "made", "disheveled", "bare_foam_stained", "empty_storage"
    has_reading_lights: bool = True         # Small bulkhead personal LED lights
    has_storage_lockers: bool = True        # Footlockers / drawers under lower bunk
    has_curtains: bool = False              # Low-poly privacy curtains
    blanket_color: str = "station_gray"     # "station_gray", "medical_blue", "emergency_orange", "brown_wool"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 480
