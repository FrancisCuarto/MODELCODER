from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class PressureDoorControlConfig(BaseAssetConfig):
    """Configuration for Pressure Door Control bulkhead access panel."""
    width: float = 0.28
    height: float = 0.42
    depth: float = 0.08
    status_light: str = "green"        # "green", "red", "yellow"
    has_keypad: bool = True
    has_card_slot: bool = True
    has_emergency_vent_button: bool = True

    name: str = "pressure_door_control"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.35
    target_tri_budget: int = 360
