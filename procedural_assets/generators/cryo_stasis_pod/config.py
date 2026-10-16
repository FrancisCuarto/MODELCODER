from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CryoStasisPodConfig(BaseAssetConfig):
    """Configuration for Cryo Stasis Pod vertical cryo-preservation chamber."""
    height: float = 2.1
    width: float = 0.85
    depth: float = 0.85
    door_open_angle: float = 0.0  # Degrees open (0.0 = sealed, 90.0 = fully open)
    frost_level: float = 0.45     # 0.0 = clear, 1.0 = heavy cryo frost
    pod_state: str = "occupied"   # "empty", "occupied", "offline"
    has_cryo_pipes: bool = True
    has_status_monitor: bool = True

    name: str = "cryo_stasis_pod"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 950
