from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class FireExtinguisherConfig(BaseAssetConfig):
    """
    Configuration for Facility Fire Extinguishers and Emergency Stations.
    Includes pressurized tanks, pressure gauges, wall cabinets with broken glass, and hoses.
    """
    tank_radius: float = 0.08
    tank_height: float = 0.45

    # Mounting & Enclosure
    mount_style: str = "wall_bracket"  # "wall_bracket", "emergency_cabinet", "floor_stand"
    cabinet_width: float = 0.36
    cabinet_height: float = 0.75
    cabinet_depth: float = 0.22
    cabinet_glass_state: str = "intact"  # "intact", "broken_shattered", "door_open"

    # Details
    has_pressure_gauge: bool = True
    has_hose_nozzle: bool = True
    has_wall_sign: bool = True  # Identification placard above extinguisher

    name: str = "fire_extinguisher"
    target_tri_budget: int = 340
    wear_level: float = 0.60
