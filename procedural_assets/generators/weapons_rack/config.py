from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class WeaponsRackConfig(BaseAssetConfig):
    """Configuration for armory weapons racks, shotgun locking bars, and riot gear lockers."""
    rack_type: str = "long_guns_vertical"    # "long_guns_vertical", "sidearm_cabinet", "stun_batons"
    width: float = 0.90                     # Rack width in meters
    depth: float = 0.40                     # Rack depth in meters
    height: float = 1.65                    # Total height in meters
    slot_count: int = 5                     # Number of weapon slots (3 to 6)
    is_locked: bool = True                  # Horizontal steel locking retainer bar with padlock
    occupancy_ratio: float = 0.60           # Percentage of slots with weapons still present
    has_bottom_ammo_box: bool = True        # Lower steel ammo chest / magazine compartment
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 360
