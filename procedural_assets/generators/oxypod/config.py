from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OxypodConfig(BaseAssetConfig):
    """Configuration for Oxypod oxygen recovery stations and portable canisters."""
    station_type: str = "wall_station"  # "wall_station", "portable_canister", "dual_tank_rig"
    tank_height: float = 0.95
    tank_radius: float = 0.18

    oxygen_level: float = 0.85  # 0.0 = depleted (red), 1.0 = full (cyan)
    has_gauge_sight: bool = True
    has_protective_cage: bool = False  # Tubular roll-cage crash bars
    has_mask_dock: bool = True
    has_coiled_hose: bool = True  # Hanging flexible umbilical hose
    has_dual_gauges: bool = True
    beacon_state: str = "cyan"  # "cyan", "green", "red", "off"

    name: str = "oxypod"
    target_tri_budget: int = 440
