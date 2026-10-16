from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class CameraMonitorConfig(BaseAssetConfig):
    """Configuration for industrial security CCTV CRT monitor with quad feed or single view."""
    name: str = "camera_monitor"
    family_id: str = "camera_monitor"
    category: str = "security"
    screen_layout: str = "quad_split"        # quad_split, single_large, dual_stack
    display_state: str = "cctv_feed"         # cctv_feed, static_noise, no_signal, standby
    has_desk_swivel_stand: bool = True
    has_control_deck: bool = True
    wear_level: float = 0.4
    target_tri_budget: int = 290

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "screen_layout": self.screen_layout,
            "display_state": self.display_state,
            "has_desk_swivel_stand": self.has_desk_swivel_stand,
            "has_control_deck": self.has_control_deck,
        })
        return d
