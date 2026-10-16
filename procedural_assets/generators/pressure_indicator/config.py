from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class PressureIndicatorConfig(BaseAssetConfig):
    """Configuration for Pressure Indicator large mural dial gauge."""
    diameter: float = 0.45
    depth: float = 0.12
    needle_angle: float = 35.0         # Degrees (-120.0 to 120.0)
    has_warning_zones: bool = True     # Colored arc zones (green/yellow/red)
    has_protective_glass: bool = True
    has_bottom_pipe_fitting: bool = True

    name: str = "pressure_indicator"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.35
    target_tri_budget: int = 280
