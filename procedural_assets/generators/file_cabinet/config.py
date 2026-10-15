from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class FileCabinetConfig(BaseAssetConfig):
    """Configuration for sheet metal lateral file cabinets, paper archives, and blueprint drawer stacks."""
    cabinet_style: str = "vertical_4_drawer" # "vertical_4_drawer", "lateral_wide", "blueprint_flat_file"
    drawer_count: int = 4                   # Number of sliding drawers (2 to 6)
    width: float = 0.50                     # Cabinet width in meters
    depth: float = 0.62                     # Cabinet depth in meters
    height: float = 1.35                    # Cabinet height in meters
    drawer_open_mode: str = "staggered_open"# "all_closed", "staggered_open", "looted_papers"
    has_label_holders: bool = True          # Stamped metal index card holder frames
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 260
