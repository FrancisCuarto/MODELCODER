from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ToolChestCartConfig(BaseAssetConfig):
    """Configuration for mobile mechanics tool chest roll-cabs and engine service carts."""
    cart_style: str = "mobile_mechanic_cart" # "mobile_mechanic_cart", "roll_cab_combo", "low_service_trolley"
    width: float = 0.70                     # Cabinet width in meters
    depth: float = 0.50                     # Depth in meters
    height: float = 0.95                    # Height from floor in meters
    drawer_count: int = 5                   # Number of tool drawers (3 to 7)
    drawer_open_style: str = "top_drawer_open" # "all_closed", "top_drawer_open", "staggered"
    has_side_handle: bool = True            # Tubular side push/pull handle
    has_top_mat_parts: bool = True          # Loose mechanical spare parts on rubber top mat
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
