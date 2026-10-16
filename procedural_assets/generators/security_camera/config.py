from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class SecurityCameraConfig(BaseAssetConfig):
    """Configuration for industrial orientable CCTV surveillance camera."""
    name: str = "security_camera"
    family_id: str = "security_camera"
    category: str = "security"
    camera_type: str = "bullet"  # bullet, dome, heavy_enclosure
    pan_angle: float = 25.0      # -75.0 to 75.0 deg
    tilt_angle: float = -20.0    # -60.0 to 10.0 deg
    has_sun_shield: bool = True
    has_status_led: bool = True
    has_ir_ring: bool = True
    mount_type: str = "wall"     # wall, ceiling, corner
    wear_level: float = 0.35
    target_tri_budget: int = 220

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "camera_type": self.camera_type,
            "pan_angle": self.pan_angle,
            "tilt_angle": self.tilt_angle,
            "has_sun_shield": self.has_sun_shield,
            "has_status_led": self.has_status_led,
            "has_ir_ring": self.has_ir_ring,
            "mount_type": self.mount_type,
        })
        return d
