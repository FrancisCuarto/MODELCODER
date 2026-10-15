from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class TerminalConfig(BaseAssetConfig):
    """Configuration for diegetic computer terminals with rich retrofuturistic variants."""
    terminal_type: str = "wall"  # "wall", "desktop", "pedestal"
    state: str = "active"  # "active", "alarm", "damaged", "powered_off"

    width: float = 0.55
    height: float = 0.65
    depth: float = 0.35

    screen_w: float = 0.36
    screen_h: float = 0.26
    phosphor_color: str = "green"  # "green", "amber", "blue_scan"
    crt_bulge: float = 0.025

    keyboard_style: str = "integrated"  # "integrated", "tray_projecting", "keypad_numeric", "none"
    has_card_reader: bool = True
    card_reader_side: str = "right"  # "right", "left"
    has_floppy_drive: bool = True  # Retro 3.5" disk or consciousness cartridge slot
    has_speaker_grill: bool = True
    has_hanging_cables: bool = True
    cable_count: int = 2

    name: str = "terminal"
    target_tri_budget: int = 450
