from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class StarChartDisplayConfig(BaseAssetConfig):
    """Configuration for large-format bridge star chart and orbital plot display."""
    name: str = "star_chart_display"
    family_id: str = "star_chart_display"
    category: str = "command"
    width: float = 1.35
    height: float = 0.85
    depth: float = 0.08
    display_mode: str = "orbital_plot"  # orbital_plot, star_map, alert_route, dark_offline
    has_control_strip: bool = True
    has_corner_brackets: bool = True
    wear_level: float = 0.3
    target_tri_budget: int = 240

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "display_mode": self.display_mode,
            "has_control_strip": self.has_control_strip,
            "has_corner_brackets": self.has_corner_brackets,
        })
        return d
