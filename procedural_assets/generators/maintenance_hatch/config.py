from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MaintenanceHatchConfig(BaseAssetConfig):
    """Configuration for Pressure-Tight Utility Maintenance Access Hatch."""
    hatch_shape: str = "square"         # "square", "octagonal_round"
    width: float = 0.80
    height: float = 0.80
    hatch_depth: float = 0.14
    open_angle: float = 0.0             # 0.0 = dogged shut, 80.0 = swung open
    dogging_mechanism: str = "central_wheel" # "central_wheel", "perimeter_latches", "quick_release"
    has_viewport: bool = False          # Small thick reinforced observation port
    has_interlock_light: bool = True    # Overhead pressure status LED interlock beacon

    name: str = "maintenance_hatch"
    pivot_rule: str = "wall_back"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 540
