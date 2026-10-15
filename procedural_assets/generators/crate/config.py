from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CrateConfig(BaseAssetConfig):
    """Configuration for industrial cargo crates, medical boxes and chemical containers."""
    crate_type: str = "cargo_chest"  # "cargo_chest", "chemical_drum", "battery_cell", "medical_crate"
    lid_state: str = "closed"  # "closed", "ajar_open", "clamped"

    width: float = 0.80
    height: float = 0.65
    depth: float = 0.60

    has_handles: bool = True
    has_reinforced_corners: bool = True
    has_latches: bool = True
    has_hazard_marking: bool = True

    name: str = "crate"
    target_tri_budget: int = 340
