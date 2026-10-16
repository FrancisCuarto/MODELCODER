from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class GeneratorUnitConfig(BaseAssetConfig):
    """Configuration for Encapsulated Auxiliary Diesel / Turbine Generator Unit."""
    gen_length: float = 1.45
    gen_width: float = 0.85
    gen_height: float = 1.15
    has_exhaust_stack: bool = True       # Vertical silenced exhaust pipe with rain cap
    has_control_panel: bool = True       # Recessed electrical starter and throttle panel
    has_service_hatch: bool = True       # Side ventilated inspection hatch
    generator_status: str = "running"    # "standby", "running", "overheat", "offline"

    name: str = "generator_unit"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.50
    target_tri_budget: int = 700
