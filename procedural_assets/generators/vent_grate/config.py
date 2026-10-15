from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class VentGrateConfig(BaseAssetConfig):
    """
    Configuration for Europa station HVAC air grilles, ventilation shafts, and floor grates.
    Survival horror escape routes: hanging grilles, visible whirring/stationary fan blades.
    """
    width: float = 0.60
    height: float = 0.60
    frame_depth: float = 0.05
    duct_depth: float = 0.25

    # Grille design & condition
    grate_type: str = "wall_louver"  # "wall_louver", "perforated_mesh", "heavy_floor_grate"
    grate_state: str = "bolted_intact"  # "bolted_intact", "hanging_by_one_screw", "removed_open_duct"
    hanging_angle: float = 28.0

    # Interior duct machinery
    has_fan_blades: bool = True
    fan_blade_count: int = 4
    fan_rotation_deg: float = 15.0

    name: str = "vent_grate"
    target_tri_budget: int = 280
    wear_level: float = 0.70
