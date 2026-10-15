from dataclasses import dataclass, field
from typing import Dict, List, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class StationRoomConfig(BaseAssetConfig):
    """Configuration for complete space station rooms, labs, and chambers."""
    room_archetype: str = "medbay_lab"    # "medbay_lab", "control_hub", "cargo_bay", "airlock_chamber", "crew_quarters"
    width: float = 6.0                    # Room width across X axis in meters
    depth: float = 8.0                    # Room depth across Y axis in meters
    height: float = 3.4                   # Ceiling clearance in meters
    door_north: bool = True               # Open doorway in +Y wall
    door_south: bool = True               # Open doorway in -Y wall
    door_east: bool = False               # Open doorway in +X wall
    door_west: bool = False               # Open doorway in -X wall
    doorway_width: float = 2.0            # Doorway opening width (matches door asset)
    doorway_height: float = 2.4           # Doorway opening height (matches door asset)
    pillar_layout: str = "perimeter_buttresses" # "none", "center_single", "dual_columns", "perimeter_buttresses"
    floor_elevation: str = "flat"         # "flat", "raised_platform", "sunken_pit"
    has_observation_window: bool = False  # Large reinforced glass viewport
    has_overhead_gantry: bool = False     # Heavy industrial yellow crane beam
    has_floor_drain: bool = False         # Center drainage grate trench
    lighting_color: str = "clean_white"   # "clean_white", "emergency_red", "medbay_cyan", "dim_amber"
    target_tri_budget: int = 750
    palette_name: str = "industrial_hazard"
    doorway_sockets: List[Dict[str, Any]] = field(default_factory=list)
