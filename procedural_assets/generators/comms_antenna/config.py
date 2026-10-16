from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class CommsAntennaConfig(BaseAssetConfig):
    """Configuration for technical radio-frequency dipole mast antenna."""
    name: str = "comms_antenna"
    family_id: str = "comms_antenna"
    category: str = "comms"
    height: float = 1.8
    mast_radius: float = 0.03
    dipole_pairs: int = 3
    arm_length: float = 0.35
    has_tuning_box: bool = True
    has_guy_wires: bool = False
    antenna_state: str = "nominal"  # nominal, folded, broken
    wear_level: float = 0.35
    target_tri_budget: int = 360

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "height": self.height,
            "mast_radius": self.mast_radius,
            "dipole_pairs": self.dipole_pairs,
            "arm_length": self.arm_length,
            "has_tuning_box": self.has_tuning_box,
            "has_guy_wires": self.has_guy_wires,
            "antenna_state": self.antenna_state,
        })
        return d
