from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class HelmetStorageConfig(BaseAssetConfig):
    """Configuration for Helmet Storage compartmentalized EVA locker."""
    height: float = 1.85
    width: float = 1.0
    depth: float = 0.55
    grid_rows: int = 3                # 2 to 4 vertical shelf tiers
    grid_cols: int = 2                # 1 to 3 horizontal columns
    helmet_density: float = 0.65      # Ratio of cubbies storing helmets
    door_style: str = "open"          # "open", "glass_door", "mesh_grate"
    has_charging_cables: bool = True
    has_status_leds: bool = True

    name: str = "helmet_storage"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.4
    target_tri_budget: int = 800
