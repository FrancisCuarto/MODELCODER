from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class AntennaDishConfig(BaseAssetConfig):
    """Configuration for steerable directional parabolic antenna dish."""
    name: str = "antenna_dish"
    family_id: str = "antenna_dish"
    category: str = "comms"
    dish_diameter: float = 0.8
    dish_depth: float = 0.18
    elevation_angle: float = 35.0  # 0 to 75 deg
    azimuth_angle: float = 20.0    # -180 to 180 deg
    has_sub_reflector: bool = True
    mount_type: str = "pedestal"    # pedestal, wall_bracket
    condition: str = "nominal"      # nominal, misaligned, damaged
    wear_level: float = 0.4
    target_tri_budget: int = 240

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "dish_diameter": self.dish_diameter,
            "dish_depth": self.dish_depth,
            "elevation_angle": self.elevation_angle,
            "azimuth_angle": self.azimuth_angle,
            "has_sub_reflector": self.has_sub_reflector,
            "mount_type": self.mount_type,
            "condition": self.condition,
        })
        return d
