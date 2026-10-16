from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class ForkliftCartConfig(BaseAssetConfig):
    """Configuration for manual pallet jack / forklift cart."""
    name: str = "forklift_cart"
    family_id: str = "forklift_cart"
    category: str = "cargo"
    fork_length: float = 1.15
    fork_spread: float = 0.55
    fork_height: float = 0.085
    tiller_angle: float = 35.0
    has_load_backrest: bool = False
    condition: str = "nominal"  # nominal, worn, derelict
    wear_level: float = 0.45
    target_tri_budget: int = 280

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "fork_length": self.fork_length,
            "fork_spread": self.fork_spread,
            "fork_height": self.fork_height,
            "tiller_angle": self.tiller_angle,
            "has_load_backrest": self.has_load_backrest,
            "condition": self.condition,
        })
        return d
