from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class TrashBinConfig(BaseAssetConfig):
    """
    Configuration for Facility Waste Bins and Biohazard Receptacles.
    Includes step pedal cans, dented industrial drums, open lids, and spilled waste bags.
    """
    bin_type: str = "pedal_can"  # "pedal_can", "drum_hazard", "office_basket"
    height: float = 0.65
    radius: float = 0.20
    is_rectangular: bool = False
    width: float = 0.38
    depth: float = 0.38

    # Lid & mechanism
    lid_state: str = "ajar"  # "closed", "ajar", "open_wide", "missing"
    lid_open_angle: float = 25.0
    has_foot_pedal: bool = True

    # Interior & contents
    has_overflowing_trash: bool = True
    has_hazard_symbol: bool = True

    name: str = "trash_bin"
    target_tri_budget: int = 320
    wear_level: float = 0.70
