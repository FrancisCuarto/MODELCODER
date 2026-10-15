from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SignPlacardConfig(BaseAssetConfig):
    """
    Configuration for Europa facility directional signage, hazard placards, and sector markers.
    Includes survival horror environmental storytelling: bent corners, snapped hanging chains, flickering lights.
    """
    width: float = 0.80
    height: float = 0.35
    depth: float = 0.04

    # Mounting method
    mount_type: str = "wall_flush"  # "wall_flush", "ceiling_hanging", "flag_perpendicular"
    hanging_chain_length: float = 0.45

    # Sign content and graphics
    sign_type: str = "hazard_biohazard"  # "hazard_biohazard", "emergency_exit", "sector_id", "high_voltage"
    has_illumination: bool = True  # Backlit stencil or fluorescent overhead light

    # Environmental damage
    damage_style: str = "bent_corner"  # "pristine", "bent_corner", "hanging_crooked"
    has_corner_bolts: bool = True

    name: str = "sign_placard"
    target_tri_budget: int = 240
    wear_level: float = 0.65
