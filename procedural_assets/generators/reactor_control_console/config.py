from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ReactorControlConsoleConfig(BaseAssetConfig):
    """Configuration for Nuclear / Thermal Reactor Master Control Console."""
    console_width: float = 1.4
    console_depth: float = 0.95
    console_height: float = 1.35
    screen_count: int = 3                # 2 to 4 upper CRT monitoring terminals
    has_scram_switch: bool = True        # Guarded red emergency SCRAM reactor trip lever
    dial_gauge_count: int = 4            # Circular analog core flux and pressure meters
    reactor_state: str = "nominal"       # "nominal", "overload", "scram", "offline"

    name: str = "reactor_control_console"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.40
    target_tri_budget: int = 750
