from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class EvaSuitStandConfig(BaseAssetConfig):
    """Configuration for EVA Suit Stand standalone maintenance and donning rig."""
    height: float = 1.95
    base_width: float = 0.8
    has_suit_mounted: bool = True       # Whether an EVA suit is currently on the stand
    arm_pose: str = "relaxed"          # "relaxed", "extended", "t_pose"
    has_service_umbilical: bool = True # Floor data and oxygen hookup umbilical
    has_diagnostic_tablet: bool = True # Articulated telemetry console tablet

    name: str = "eva_suit_stand"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 700
