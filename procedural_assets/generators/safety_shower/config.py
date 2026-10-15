from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SafetyShowerConfig(BaseAssetConfig):
    """Configuration for chemical emergency drench showers, eyewash stations, and decontamination poles."""
    shower_type: str = "combined_shower_eyewash" # "combined_shower_eyewash", "eyewash_pedestal", "decon_station_curtain"
    width: float = 0.75                         # Footprint width in meters
    depth: float = 0.85                         # Footprint depth in meters
    height: float = 2.25                        # Deluge shower head height in meters
    has_pull_chain: bool = True                 # Triangular pull-down actuator ring & rod
    has_eyewash_bowl: bool = True               # Waist-level stainless basin with spray nozzles
    has_floor_drain_grate: bool = True          # Integrated floor drain basin
    has_hazard_stripes: bool = True             # High-visibility yellow/black warning sign
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 280
