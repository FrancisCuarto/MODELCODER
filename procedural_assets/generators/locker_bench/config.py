from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class LockerBenchConfig(BaseAssetConfig):
    """Configuration for locker room benches, airlock changing seats, and boot rack benches."""
    bench_type: str = "perforated_metal"    # "perforated_metal", "composite_slats", "boot_rack_integrated"
    length: float = 1.60                    # Bench length in meters
    width: float = 0.45                     # Seat depth in meters
    height: float = 0.48                    # Seat height in meters
    has_shoe_shelf: bool = True             # Lower wire grid shelf for magnetic boots
    leg_style: str = "tubular_flanged"      # "tubular_flanged", "slab_sides"
    has_forgotten_gear: bool = True         # Left-behind boots or rolled emergency towel
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 300
