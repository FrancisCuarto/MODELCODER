from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ConsciousnessArchiveConfig(BaseAssetConfig):
    """Configuration for Consciousness Archive memory cartridge bank."""
    height: float = 2.0
    width: float = 1.0
    depth: float = 0.7
    bay_rows: int = 4              # 2 to 6 rows of cartridge shelves
    cartridge_density: float = 0.75 # 0.0 to 1.0 ratio of slots filled
    has_cooling_vent: bool = True
    has_conduit_harness: bool = True

    name: str = "consciousness_archive"
    palette_name: str = "command_bridge"
    wear_level: float = 0.4
    target_tri_budget: int = 900
