from dataclasses import dataclass, field
from typing import Dict, List, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class StationCorridorConfig(BaseAssetConfig):
    """Configuration for modular industrial space station corridors."""
    corridor_type: str = "straight"       # "straight", "corner_90", "t_junction", "cross_junction", "doorway_arch", "dead_end"
    width: float = 3.0                   # Internal corridor width in meters
    length: float = 4.0                  # Segment length in meters
    height: float = 3.0                  # Floor-to-ceiling clearance in meters
    floor_style: str = "tread_plate"     # "tread_plate", "grated_trench", "smooth_tile"
    wall_style: str = "structural_ribs"  # "structural_ribs", "recessed_panels", "smooth_bulkhead"
    ceiling_style: str = "exposed_beams" # "exposed_beams", "vaulted_conduit", "flat_recessed"
    has_integrated_lighting: bool = True
    lighting_state: str = "working"      # "working", "flickering", "emergency_red", "unlit"
    has_cable_runs: bool = True
    has_wall_alcove: bool = True         # Inset niche for mounting station props
    has_hazard_stripes: bool = True      # Floor edge caution stripes
    damage_state: str = "pristine"       # "pristine", "blood_oil_stain", "collapsed_ceiling_wires", "breached_vent"
    doorway_width: float = 2.0           # Standard opening width for bulkhead doors
    doorway_height: float = 2.4          # Standard opening height for bulkhead doors
    target_tri_budget: int = 550
    palette_name: str = "industrial_hazard"
    connection_sockets: List[Dict[str, Any]] = field(default_factory=list)
