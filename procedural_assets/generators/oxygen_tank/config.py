from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OxygenTankConfig(BaseAssetConfig):
    """Configuration for Oxygen Tank industrial compressed gas cylinder."""
    tank_height: float = 1.1
    tank_radius: float = 0.14
    tank_color: str = "cyan"           # "cyan", "white", "yellow"
    has_top_handle_cage: bool = True   # Roll cage protecting the brass valve
    has_mini_gauge: bool = True        # Neck pressure indicator dial
    has_hazard_collar: bool = True     # Contrast stripe around cylinder neck

    name: str = "oxygen_tank"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.35
    target_tri_budget: int = 340
