from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class EmergencyBeaconConfig(BaseAssetConfig):
    """Configuration for rotating or flashing industrial hazard beacon."""
    name: str = "emergency_beacon"
    family_id: str = "emergency_beacon"
    category: str = "security"
    beacon_color: str = "amber"          # amber, red, blue, green
    base_style: str = "flange"           # flange, pedestal, magnetic
    has_protective_cage: bool = True
    lens_shape: str = "dome"             # dome, cylindrical_fresnel
    is_active: bool = True
    wear_level: float = 0.35
    target_tri_budget: int = 280

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "beacon_color": self.beacon_color,
            "base_style": self.base_style,
            "has_protective_cage": self.has_protective_cage,
            "lens_shape": self.lens_shape,
            "is_active": self.is_active,
        })
        return d
