from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SuitRackConfig(BaseAssetConfig):
    """Configuration for Suit Rack EVA spacesuit storage assembly."""
    width: float = 1.4
    height: float = 1.9
    depth: float = 0.65
    suit_positions: int = 3           # 2 to 4 suit hanging stations
    occupied_suits: int = 2           # Number of suits currently hung
    has_boot_tray: bool = True        # Lower drip grating tray
    has_helmet_hooks: bool = True     # Upper helmet peg brackets

    name: str = "suit_rack"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.4
    target_tri_budget: int = 750
