from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class FuseBoxConfig(BaseAssetConfig):
    """Configuration for Wall-Mounted Industrial Electrical Fuse Box."""
    box_width: float = 0.55
    box_height: float = 0.70
    box_depth: float = 0.22
    door_open_angle: float = 0.0        # 0.0 = closed and latched, 85.0 = fully open
    fuse_rows: int = 2                  # 1 to 3 horizontal fuse holder rails
    fuses_per_row: int = 4              # 3 to 5 ceramic cartridge fuses per rail
    missing_fuse: bool = False          # One fuse socket is blown / missing cartridge
    has_main_switch: bool = True        # Heavy exterior cutoff switch lever on side

    name: str = "fuse_box"
    pivot_rule: str = "wall_back"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 520
