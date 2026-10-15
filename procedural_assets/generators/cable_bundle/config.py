from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CableBundleConfig(BaseAssetConfig):
    """
    Configuration for sprawling Europa facility industrial wiring, sagging umbilical cables,
    and wall/ceiling cable tray raceways.
    """
    length: float = 2.0
    bundle_type: str = "hanging_umbilical"  # "hanging_umbilical", "ladder_rack_tray", "vertical_riser"
    cable_count: int = 4
    max_sag: float = 0.28

    # Environmental hazards
    has_severed_wire: bool = False  # Broken wire cut and dangling
    has_support_ties: bool = True  # Steel band zip ties holding bundle together
    has_junction_box: bool = True  # Wall breakout terminal junction box at start

    name: str = "cable_bundle"
    target_tri_budget: int = 320
    wear_level: float = 0.65
