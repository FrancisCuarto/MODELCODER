from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ChemicalCabinetConfig(BaseAssetConfig):
    """Configuration for toxic chemical storage, medicine display cases, and specimen cabinets."""
    cabinet_type: str = "tall_two_door"     # "tall_two_door", "low_counter_top", "wall_hanging"
    width: float = 0.90                     # Overall cabinet width in meters
    height: float = 1.80                    # Overall cabinet height in meters
    depth: float = 0.45                     # Overall cabinet depth in meters
    glass_type: str = "wired_mesh"          # "wired_mesh", "frosted_hazard", "missing_broken"
    door_state: str = "both_closed"         # "both_closed", "left_open", "right_ajar"
    has_padlock: bool = True                # Heavy hasp with hanging padlock
    shelf_item_density: float = 0.70        # Reagent bottle and specimen canister clutter (0.0 to 1.0)
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 450
