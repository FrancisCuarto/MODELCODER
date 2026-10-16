from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CoolantPipeJunctionConfig(BaseAssetConfig):
    """Configuration for Modular Multi-Way Coolant Distribution Manifold / Junction."""
    pipe_diameter: float = 0.22
    junction_type: str = "cross_4way"    # "tee_3way", "cross_4way"
    arm_length: float = 0.70             # Center-to-flange branch length
    has_isolation_valves: bool = True    # Gate valves with cast handwheels on branches
    has_pressure_sensor: bool = True     # Dial manometer port on central cross hub
    has_thermal_insulation: bool = True  # Cladded thermal lagging jackets with metal band straps

    name: str = "coolant_pipe_junction"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 580
