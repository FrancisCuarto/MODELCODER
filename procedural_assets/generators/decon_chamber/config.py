from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class DeconChamberConfig(BaseAssetConfig):
    """Configuration for Decon Chamber chemical decontamination shower booth."""
    chamber_width: float = 1.2
    chamber_depth: float = 1.2
    chamber_height: float = 2.2
    door_open_angle: float = 0.0       # 0.0 = sealed door, 90.0 = fully open
    nozzle_tiers: int = 3             # 2 to 4 vertical spray rings
    has_ceiling_shower_head: bool = True
    has_external_cycle_panel: bool = True
    cycle_state: str = "idle"         # "idle", "active", "alarm"

    name: str = "decon_chamber"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 950
