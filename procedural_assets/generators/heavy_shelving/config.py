from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class HeavyShelvingConfig(BaseAssetConfig):
    """Configuration for slotted angle-iron warehouse shelving racks, cargo depot tiers, and drum stands."""
    shelf_type: str = "cargo_storage"       # "cargo_storage", "chemical_drums_rack", "empty_looted"
    width: float = 1.20                     # Shelf bay width in meters
    depth: float = 0.55                     # Shelf bay depth in meters
    height: float = 2.00                    # Total upright height in meters
    levels: int = 4                         # Number of horizontal shelf tiers (3 to 5)
    has_x_bracing: bool = True              # Rear diagonal tension wire cross-braces
    has_retaining_bars: bool = True         # Front retaining crossbars against zero-g / seismic dislodging
    bent_shelf_index: int = -1              # -1 for none, or tier index (0..levels-1) for a warped sagging shelf
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 420
