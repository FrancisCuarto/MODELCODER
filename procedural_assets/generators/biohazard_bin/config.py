from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class BiohazardBinConfig(BaseAssetConfig):
    """Configuration for Clinical Biohazard Waste Step-Can with Foot Pedal."""
    bin_diameter: float = 0.45
    bin_height: float = 0.72
    lid_open_angle: float = 0.0          # 0.0 = closed/sealed, 65.0 = fully open via pedal
    has_foot_pedal: bool = True          # Stamped steel foot lever at front base
    has_inner_bag_lip: bool = True       # Visible yellow/orange biohazard bag draped over rim
    has_side_handles: bool = True        # Folding carrying handles on left and right
    hazard_symbol: str = "biohazard"     # "biohazard", "radiation", "chemical"

    name: str = "biohazard_bin"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.40
    target_tri_budget: int = 450
