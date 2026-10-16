from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class WaterRecyclerConfig(BaseAssetConfig):
    """Configuration for graywater filtration and reverse-osmosis recycling unit."""
    name: str = "water_recycler"
    family_id: str = "water_recycler"
    category: str = "engineering"
    height: float = 1.6
    width: float = 0.95
    depth: float = 0.65
    filter_stage_count: int = 3
    has_purity_monitor: bool = True
    has_bypass_valves: bool = True
    recycler_state: str = "nominal"  # nominal, filter_saturated, emergency_bypass, derelict
    wear_level: float = 0.4
    target_tri_budget: int = 420

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "filter_stage_count": self.filter_stage_count,
            "has_purity_monitor": self.has_purity_monitor,
            "has_bypass_valves": self.has_bypass_valves,
            "recycler_state": self.recycler_state,
        })
        return d
