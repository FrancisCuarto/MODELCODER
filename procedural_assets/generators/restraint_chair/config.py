from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class RestraintChairConfig(BaseAssetConfig):
    """Configuration for interrogation chairs, medical detention seats, and heavy padded restraint thrones."""
    chair_type: str = "bolted_steel_chair"  # "bolted_steel_chair", "interrogation_throne", "detox_seat"
    width: float = 0.70                     # Seat & armrest width in meters
    depth: float = 0.75                     # Depth in meters
    height: float = 1.10                    # Backrest top height in meters
    headrest_restraint: bool = True         # Padded headrest with forehead strap
    arm_straps: str = "buckled"             # "buckled", "loose", "torn"
    leg_shackles: bool = True               # Heavy steel ankle shackles on front legs
    iv_pole: bool = True                    # Attached rear IV infusion drip pole
    floor_mounting_plate: bool = True       # Heavy bolted floor flange plate
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
