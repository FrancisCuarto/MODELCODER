from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class NavConsoleConfig(BaseAssetConfig):
    """Configuration for orbital navigation and telemetry bridge console."""
    name: str = "nav_console"
    family_id: str = "nav_console"
    category: str = "command"
    width: float = 1.4
    depth: float = 0.95
    height: float = 1.15
    screen_count: int = 3
    has_joystick: bool = True
    has_throttle: bool = True
    has_footrest: bool = True
    console_state: str = "active"  # active, standby, signal_lost, offline
    wear_level: float = 0.35
    target_tri_budget: int = 300

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "screen_count": self.screen_count,
            "has_joystick": self.has_joystick,
            "has_throttle": self.has_throttle,
            "has_footrest": self.has_footrest,
            "console_state": self.console_state,
        })
        return d
