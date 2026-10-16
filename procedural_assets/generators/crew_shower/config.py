from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class CrewShowerConfig(BaseAssetConfig):
    """Configuration for compact crew sanitation shower cubicle."""
    name: str = "crew_shower"
    family_id: str = "crew_shower"
    category: str = "habitation"
    width: float = 0.90
    depth: float = 0.90
    height: float = 2.10
    has_curtain: bool = True
    has_grab_rail: bool = True
    shower_head_type: str = "fixed_overhead"  # fixed_overhead, handheld_hose
    condition: str = "nominal"               # nominal, dry_derelict, lime_stained
    wear_level: float = 0.35
    target_tri_budget: int = 340

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "has_curtain": self.has_curtain,
            "has_grab_rail": self.has_grab_rail,
            "shower_head_type": self.shower_head_type,
            "condition": self.condition,
        })
        return d
