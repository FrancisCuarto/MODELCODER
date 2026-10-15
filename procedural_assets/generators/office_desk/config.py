from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OfficeDeskConfig(BaseAssetConfig):
    """
    Configuration for Retrofuturistic Industrial Office & Laboratory Desks.
    Used across Europa facility control rooms, research labs, and maintenance outposts.
    """
    # Main desk dimensions in meters
    width: float = 1.40
    height: float = 0.76
    depth: float = 0.75
    desktop_thickness: float = 0.04

    # Leg & structural framing
    leg_style: str = "tubular_four_legs"  # "tubular_four_legs", "panel_sides", "cantilever_t_frame"
    leg_thickness: float = 0.045

    # Storage & Pedestals
    pedestal_layout: str = "right_only"  # "none", "left_only", "right_only", "dual_pedestals"
    drawer_count_per_pedestal: int = 3
    drawer_open_style: str = "top_open"  # "all_closed", "top_open", "all_ajar"
    drawer_slide_max: float = 0.20

    # Ergonomic & station fixtures
    has_cable_grommet: bool = True
    has_partition_screen: bool = False
    partition_height: float = 0.35
    has_under_shelf: bool = True
    has_rear_cable_raceway: bool = True

    # Surface & visual styling
    surface_material: str = "metal_dark"  # "metal_dark", "beige_formica", "hazard"
    name: str = "office_desk"
    target_tri_budget: int = 420
    wear_level: float = 0.60
