from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class WallClockConfig(BaseAssetConfig):
    """Configuration for industrial bulkhead wall clock."""
    name: str = "wall_clock"
    family_id: str = "wall_clock"
    category: str = "habitation"
    diameter: float = 0.30
    depth: float = 0.05
    bezel_type: str = "circular"  # circular, octagonal
    clock_state: str = "running"  # running, stopped, broken
    hour: int = 14
    minute: int = 45
    has_glass: bool = True
    has_wall_bracket: bool = True
    wear_level: float = 0.25
    target_tri_budget: int = 280

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "diameter": self.diameter,
            "depth": self.depth,
            "bezel_type": self.bezel_type,
            "clock_state": self.clock_state,
            "hour": self.hour,
            "minute": self.minute,
            "has_glass": self.has_glass,
            "has_wall_bracket": self.has_wall_bracket,
        })
        return d
