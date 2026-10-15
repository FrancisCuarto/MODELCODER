from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class DoorConfig(BaseAssetConfig):
    """Configuration for industrial doors, airlocks and emergency bulkheads."""
    door_type: str = "standard_sliding"  # "standard_sliding", "heavy_airlock", "emergency_bulkhead", "manual_hatch"
    width: float = 2.00
    height: float = 2.40
    frame_depth: float = 0.35
    frame_thickness: float = 0.18

    open_ratio: float = 0.0  # 0.0 = closed, 0.15 = jammed/ajar, 1.0 = fully open
    access_interface: str = "card_reader"  # "card_reader", "keypad_console", "manual_wheel", "none"
    has_reinforced_window: bool = True  # Viewport window into adjacent section
    has_hazard_stripes: bool = True
    has_hydraulic_pistons: bool = True  # Visible pneumatic/hydraulic rams above door
    has_status_light: bool = True

    name: str = "station_door"
    target_tri_budget: int = 480
