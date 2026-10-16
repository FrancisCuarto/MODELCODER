from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ServiceLiftDoorConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial Freight Elevator / Service Lift Door."""
    door_width: float = 1.80
    door_height: float = 2.40
    frame_depth: float = 0.25
    door_state: str = "closed"          # "closed", "open_partial", "jammed_open", "maintenance_locked"
    has_call_station: bool = True       # Wall-mounted hall call box with floor indicator and key switch
    has_capacity_sign: bool = True      # Heavy SWL 5000 KG load capacity warning placard
    has_toe_guard_kickplate: bool = True # Ribbed steel diamond kickplate on lower door panels

    name: str = "service_lift_door"
    pivot_rule: str = "wall_back"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 620
