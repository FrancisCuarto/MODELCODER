from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class FoodStorageUnitConfig(BaseAssetConfig):
    """Configuration for pressurized crew ration and food supply storage cabinet."""
    name: str = "food_storage_unit"
    family_id: str = "food_storage_unit"
    category: str = "habitation"
    height: float = 1.75
    width: float = 0.85
    depth: float = 0.55
    compartment_rows: int = 4
    has_latch_bars: bool = True
    has_ration_trays: bool = True
    storage_state: str = "stocked"  # stocked, depleted, open_looted
    wear_level: float = 0.35
    target_tri_budget: int = 250

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "compartment_rows": self.compartment_rows,
            "has_latch_bars": self.has_latch_bars,
            "has_ration_trays": self.has_ration_trays,
            "storage_state": self.storage_state,
        })
        return d
