from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class NightstandConfig(BaseAssetConfig):
    """Configuration for crew bedside lockers, nightstands, and medical side tables."""
    stand_type: str = "crew_locker_cubby"   # "crew_locker_cubby", "sliding_drawers", "medical_tray_cart", "wall_mounted"
    width: float = 0.48                    # Width in meters
    depth: float = 0.44                    # Depth in meters
    height: float = 0.68                   # Cabinet height in meters
    drawer_count: int = 2                  # Number of drawers (1-3)
    drawer_open_ratio: float = 0.0         # 0.0 closed, 0.4 half open
    has_raised_rim: bool = True            # Anti-slide retaining lip on tabletop
    has_bedside_lamp: bool = True          # Small gooseneck reading lamp
    lamp_state: str = "on"                 # "on", "off", "flickering"
    has_swivel_tray: bool = False          # Cantilevered over-bed hospital tray arm
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 340
