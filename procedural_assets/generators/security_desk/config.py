from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SecurityDeskConfig(BaseAssetConfig):
    """Configuration for checkpoint security desks, intake barrier counters, and guard stations."""
    desk_style: str = "corner_checkpoint"   # "corner_checkpoint", "straight_barrier", "intake_counter"
    width: float = 1.80                     # Desk width in meters
    depth: float = 0.90                     # Desk depth in meters
    height: float = 1.15                    # Counter height in meters
    bulletproof_glass: bool = True          # Transparent bulletproof screen partition
    has_intercom_grille: bool = True        # Speaker grille and document pass-through tray
    has_cctv_monitor: bool = True           # Arm-mounted surveillance CRT monitor
    has_under_counter_shelf: bool = True    # Shelf with alarm button and weapon holster
    glass_damage: str = "intact"            # "intact", "bullet_spall", "smashed"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 340
