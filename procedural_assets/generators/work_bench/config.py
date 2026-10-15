from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class WorkBenchConfig(BaseAssetConfig):
    """Configuration for engineering workbenches, maintenance tables, and tool stations."""
    bench_type: str = "standard_workbench"  # "standard_workbench", "heavy_machinist", "electronics_soldering"
    width: float = 1.80                     # Workbench width in meters
    depth: float = 0.85                     # Depth in meters
    height: float = 0.90                    # Worktop height in meters
    has_pegboard: bool = True               # Rear upright tool hanging board
    has_vise: bool = True                   # Heavy bench vise clamp
    has_under_shelf: bool = True            # Lower storage shelf
    has_overhead_light: bool = True         # Cantilevered task luminaire
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 340
