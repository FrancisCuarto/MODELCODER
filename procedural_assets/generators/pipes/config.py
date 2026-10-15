from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class PipeConfig(BaseAssetConfig):
    """Configuration for industrial pipe networks, elbows, valves and bypasses."""
    pipe_type: str = "valve_assembly"  # "valve_assembly", "straight", "elbow_90", "t_junction"
    radius: float = 0.09
    length: float = 1.80

    valve_type: str = "handwheel_red"  # "handwheel_red", "lever_quarter_turn", "none"
    has_pressure_gauge: bool = True
    has_insulation_layer: bool = False  # Thermal lagging insulation jacket
    has_flange_couplings: bool = True

    name: str = "pipe_assembly"
    target_tri_budget: int = 400
