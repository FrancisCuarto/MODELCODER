from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class ConveyorSegmentConfig(BaseAssetConfig):
    """Configuration for industrial modular conveyor segment (straight or inclined)."""
    name: str = "conveyor_segment"
    family_id: str = "conveyor_segment"
    category: str = "cargo"
    length: float = 2.0
    width: float = 0.8
    height: float = 0.75
    incline_angle: float = 0.0
    roller_density: int = 10
    has_side_rails: bool = True
    has_motor: bool = True
    conveyor_type: str = "rollers"  # rollers, belt, powered_incline
    wear_level: float = 0.4
    target_tri_budget: int = 500

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "incline_angle": self.incline_angle,
            "roller_density": self.roller_density,
            "has_side_rails": self.has_side_rails,
            "has_motor": self.has_motor,
            "conveyor_type": self.conveyor_type,
        })
        return d
