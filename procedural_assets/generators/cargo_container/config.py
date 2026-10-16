from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CargoContainerConfig(BaseAssetConfig):
    """Configuration for Standardized Interstellar Logistics Cargo Container."""
    container_length: float = 2.40
    container_width: float = 1.30
    container_height: float = 1.40
    corrugation_ribs: int = 5           # 3 to 8 structural corrugated side wall ribs
    doors_open_angle: float = 0.0       # 0.0 = dogged shut, 85.0 = swung open
    has_forklift_pockets: bool = True   # Bottom transverse rectangular sleeves for forklift tines
    cargo_class: str = "general_supplies" # "general_supplies", "cryo_hazard", "armory_munitions"
    container_condition: str = "nominal" # "nominal", "dented_impact", "derelict_rusted"

    name: str = "cargo_container"
    pivot_rule: str = "floor_center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 650
