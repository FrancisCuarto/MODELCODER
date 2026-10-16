from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SurgicalLightConfig(BaseAssetConfig):
    """Configuration for Articulated Multi-Reflector Operating Room Surgical Light."""
    dish_diameter: float = 0.75
    reflector_count: int = 4            # 3 to 6 circular faceted light lenses
    arm_reach: float = 1.25             # Reach distance of the dual articulating suspension arm
    arm_pitch_deg: float = -20.0        # Arm downward angle (-45 to +20 degrees)
    dish_pitch_deg: float = 30.0        # Lamp head tilt down toward operating field
    dish_yaw_deg: float = 15.0          # Lamp head rotation angle
    is_light_on: bool = True            # Light reflectors emit brilliant surgical illumination
    has_central_handle: bool = True     # Central detachable sterile steering handle
    mount_type: str = "ceiling"         # "ceiling", "wall"

    name: str = "surgical_light"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.25
    target_tri_budget: int = 680
