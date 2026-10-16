from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class BiometricScannerConfig(BaseAssetConfig):
    """Configuration for palm/fingerprint biometric access terminal."""
    name: str = "biometric_scanner"
    family_id: str = "biometric_scanner"
    category: str = "security"
    scanner_type: str = "palm_pad"         # palm_pad, fingerprint_dock, multi_auth
    mount_style: str = "wall"              # wall, pedestal
    scan_state: str = "active_laser"       # idle, active_laser, verified, alarm
    has_face_reticle: bool = True
    has_intercom_mic: bool = True
    wear_level: float = 0.35
    target_tri_budget: int = 240

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "scanner_type": self.scanner_type,
            "mount_style": self.mount_style,
            "scan_state": self.scan_state,
            "has_face_reticle": self.has_face_reticle,
            "has_intercom_mic": self.has_intercom_mic,
        })
        return d
