from dataclasses import dataclass, field
from typing import List
from ...core.base_config import BaseAssetConfig

@dataclass
class CrashCartConfig(BaseAssetConfig):
    """
    Configuration for Industrial/Medical Emergency Crash Cart.
    Faithfully replicates the PS1 retro-survival horror aesthetic from Below Nominal.
    """
    # Main cart chassis dimensions (in meters)
    width: float = 0.65
    height: float = 0.85
    depth: float = 0.48

    # Drawer system
    drawer_count: int = 4
    drawer_open_mode: str = "staggered"  # "all_closed", "staggered", "top_open", "all_open"
    drawer_slide_max: float = 0.22  # Maximum drawer extension in meters
    drawer_handle_style: str = "metal_bar"  # "metal_bar", "recessed_lip", "industrial_latch"

    # Top Defibrillator / CRT Monitor Unit
    has_top_monitor: bool = True
    monitor_width: float = 0.34
    monitor_height: float = 0.22
    monitor_depth: float = 0.28
    monitor_phosphor_color: str = "green"  # "green", "amber", "off"
    has_monitor_handle: bool = True
    has_monitor_knobs: bool = True

    # Side Accessories & Ergonomics
    has_push_handle: bool = True
    push_handle_side: str = "left"  # "left", "right"
    has_oxygen_rack: bool = True
    oxygen_tank_count: int = 1  # 1 or 2 cylinders
    has_corner_bumpers: bool = True
    has_hazard_stripes: bool = True

    # Running Gear (Wheels / Casters)
    caster_style: str = "swivel"  # "swivel", "rigid", "skid_feet"
    caster_radius: float = 0.045
    caster_height: float = 0.10

    # Aesthetics and Style
    body_color_preset: str = "red_emergency"  # "red_emergency", "dirty_beige", "hazard_yellow"
    name: str = "crash_cart"
    target_tri_budget: int = 580
    wear_level: float = 0.65
