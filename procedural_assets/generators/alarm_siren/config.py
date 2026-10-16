from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class AlarmSirenConfig(BaseAssetConfig):
    """Configuration for industrial alarm siren with acoustic horn and strobe beacon."""
    name: str = "alarm_siren"
    family_id: str = "alarm_siren"
    category: str = "security"
    siren_type: str = "horn_and_strobe"  # horn_and_strobe, dual_horn, motor_siren
    strobe_color: str = "red"            # red, amber, blue
    has_wire_guard: bool = True
    mount_orientation: str = "wall"      # wall, ceiling
    is_active: bool = True
    wear_level: float = 0.4
    target_tri_budget: int = 250

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "siren_type": self.siren_type,
            "strobe_color": self.strobe_color,
            "has_wire_guard": self.has_wire_guard,
            "mount_orientation": self.mount_orientation,
            "is_active": self.is_active,
        })
        return d
