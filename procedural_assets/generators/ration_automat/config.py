from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class RationAutomatConfig(BaseAssetConfig):
    """Configuration for brutalist automatic food dispensaries, ration automats, and vending machines."""
    machine_type: str = "nutrient_paste"    # "nutrient_paste", "synthetic_cigarettes", "hot_caffeine"
    width: float = 0.85                     # Cabinet width in meters
    height: float = 1.95                    # Cabinet height in meters
    depth: float = 0.65                     # Cabinet depth in meters
    dispenser_state: str = "normal"         # "normal", "jammed_door", "smashed_glass"
    display_color: str = "amber"            # "green", "amber", "dim_red"
    has_keypad: bool = True                 # Numeric selection keypad
    has_coin_card_slot: bool = True         # Credit chit / keycard reader slot
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
