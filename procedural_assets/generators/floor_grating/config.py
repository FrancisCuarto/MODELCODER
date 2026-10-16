from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class FloorGratingConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial Floor Trench Grating."""
    panel_length: float = 1.00
    panel_width: float = 1.00
    grate_depth: float = 0.06
    bar_density: int = 8                # 5 to 12 longitudinal load-bearing grating bars
    is_raised: bool = False             # Trench cover propped open at an angle
    has_recessed_frame: bool = True     # Outer recessed cast curb frame
    has_warning_stripe: bool = True     # Yellow/black perimeter warning border
    trench_state: str = "flush"         # "flush", "propped_open", "corroded_bent"

    name: str = "floor_grating"
    pivot_rule: str = "floor_center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.50
    target_tri_budget: int = 460
