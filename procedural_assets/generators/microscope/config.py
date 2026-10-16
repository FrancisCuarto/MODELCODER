from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MicroscopeConfig(BaseAssetConfig):
    """Configuration for Clinical Laboratory Optical Compound Microscope."""
    total_height: float = 0.48
    objective_count: int = 3            # 3 or 4 rotating turret objectives
    eyepiece_type: str = "binocular"    # "monocular", "binocular"
    has_slide_on_stage: bool = True     # Glass specimen slide clipped onto mechanical stage
    is_illuminator_on: bool = True      # Sub-stage condenser lamp beam illuminated
    stage_elevation: float = 0.55       # Relative vertical position of stage (focus adjustment)

    name: str = "microscope"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.25
    target_tri_budget: int = 620
