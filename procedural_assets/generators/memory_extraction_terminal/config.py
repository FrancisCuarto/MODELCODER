from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MemoryExtractionTerminalConfig(BaseAssetConfig):
    """Configuration for Memory Extraction Terminal workstation."""
    mount_style: str = "pedestal"      # "pedestal", "desktop"
    crt_tilt: float = 20.0             # Degrees tilted back
    screen_color: str = "amber"        # "amber", "green", "off"
    cartridge_inserted: bool = True
    has_side_tape_drive: bool = True
    has_rotary_dials: bool = True

    name: str = "memory_extraction_terminal"
    palette_name: str = "command_bridge"
    wear_level: float = 0.4
    target_tri_budget: int = 680
