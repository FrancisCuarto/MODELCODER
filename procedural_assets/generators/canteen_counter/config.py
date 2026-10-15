from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CanteenCounterConfig(BaseAssetConfig):
    """Configuration for mess hall service counters, food hatches, and cafeteria steam tables."""
    counter_type: str = "service_hatch"     # "service_hatch", "buffet_island", "tray_slider_station"
    width: float = 1.80                     # Counter width in meters
    depth: float = 0.80                     # Depth in meters
    height: float = 1.10                    # Service counter height in meters
    roll_up_shutter: str = "half_open"      # "closed", "half_open", "open"
    has_tray_rails: bool = True             # Tubular front rails for sliding cafeteria trays
    has_steam_pans: bool = True             # Inset bain-marie stainless food warming wells
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 320
