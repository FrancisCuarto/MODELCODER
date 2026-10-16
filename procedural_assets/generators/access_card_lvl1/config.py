from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class AccessCardConfig(BaseAssetConfig):
    width: float = 0.085
    height: float = 0.055
    thickness: float = 0.004
    chip_size: float = 0.015
    palette_name: str = "industrial_hazard"
