from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CableTrayConfig(BaseAssetConfig):
    """Configuration for Industrial Overhead Wire-Mesh / Ladder Cable Tray."""
    tray_length: float = 2.00
    tray_width: float = 0.45
    tray_height: float = 0.10
    rung_spacing: float = 0.25          # Distance between cross rungs along length
    has_cover: bool = False             # Top slotted metal dust cover plate
    has_suspension_rods: bool = True    # Ceiling threaded suspension drop rods with mounting brackets
    cable_density: float = 0.70         # Fill density of power and data cables (0.0 to 1.0)
    has_hanging_cables: bool = True     # Dangling or sagging loose secondary wires

    name: str = "cable_tray"
    pivot_rule: str = "center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 520
