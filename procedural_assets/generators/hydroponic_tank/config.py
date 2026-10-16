from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class HydroponicTankConfig(BaseAssetConfig):
    """Configuration for botanical nutrient solution hydroponic reservoir tank."""
    name: str = "hydroponic_tank"
    family_id: str = "hydroponic_tank"
    category: str = "hydroponics"
    tank_height: float = 1.3
    tank_radius: float = 0.40
    liquid_level: float = 0.75  # 0.0 to 1.0 fraction
    tank_shape: str = "cylindrical"  # cylindrical, rectangular
    has_sight_glass: bool = True
    has_feed_pipes: bool = True
    solution_type: str = "nutrient_rich"  # nutrient_rich, low_reserve, algae_bloom
    wear_level: float = 0.4
    target_tri_budget: int = 320

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "tank_height": self.tank_height,
            "tank_radius": self.tank_radius,
            "liquid_level": self.liquid_level,
            "tank_shape": self.tank_shape,
            "has_sight_glass": self.has_sight_glass,
            "has_feed_pipes": self.has_feed_pipes,
            "solution_type": self.solution_type,
        })
        return d
