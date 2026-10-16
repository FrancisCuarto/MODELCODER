from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OverheadPipeSupportConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial Overhead Trapeze Pipe Support."""
    hanger_width: float = 1.10
    drop_height: float = 0.85
    pipe_tier_count: int = 1            # 1 or 2 horizontal trapeze unistrut tiers
    pipe_slots: int = 3                 # 2 to 4 pipe clamp positions per tier
    has_pipes_included: bool = True     # Longitudinal process pipes passing through clamps
    has_beam_clamps: bool = True        # Top I-beam flange attachment clamp shoes
    hanger_state: str = "nominal"       # "nominal", "bent_overload", "missing_clamp"

    name: str = "overhead_pipe_support"
    pivot_rule: str = "center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 480
