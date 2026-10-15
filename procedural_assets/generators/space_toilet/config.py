from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SpaceToiletConfig(BaseAssetConfig):
    """Configuration for brutalist stainless steel vacuum space toilets, zero-G clamp latrines, and sanitaries."""
    toilet_type: str = "bulkhead_vacuum"    # "bulkhead_vacuum", "compact_cubicle", "zero_g_clamp"
    width: float = 0.50                     # Toilet bowl unit width in meters
    depth: float = 0.65                     # Overall projection depth in meters
    height: float = 0.85                    # Back wall tank/shroud height in meters
    has_thigh_restraints: bool = True       # Padded zero-G thigh restraint bars / handles
    lid_state: str = "closed"               # "closed", "open", "damaged"
    has_paper_dispenser: bool = True        # Wall-mounted enclosed institutional paper box
    vacuum_pipe: bool = True                # High-pressure vacuum suction waste conduit
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 240
