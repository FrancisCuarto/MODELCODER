from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class AirlockChamberConfig(BaseAssetConfig):
    """Configuration for Airlock Chamber modular decompression transition room."""
    chamber_length: float = 3.2
    chamber_width: float = 2.4
    chamber_height: float = 2.4
    inner_door_open: float = 0.0       # 0.0 to 1.0 fraction open
    outer_door_open: float = 0.0       # 0.0 to 1.0 fraction open
    has_floor_grate: bool = True
    has_depressurize_vents: bool = True
    has_eva_grab_bars: bool = True

    name: str = "airlock_chamber"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.4
    target_tri_budget: int = 1400
