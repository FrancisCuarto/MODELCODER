from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class LabWorkstationConfig(BaseAssetConfig):
    """Configuration for Modular Laboratory Research Workstation."""
    width: float = 1.6
    depth: float = 0.8
    height: float = 1.8                  # Counter height ~0.9m, top of reagent shelf ~1.8m
    has_sink: bool = True               # Chemical wash basin and tall gooseneck faucet
    has_upper_shelf: bool = True        # Multi-tier reagent bottle and rack shelving
    has_terminal_screen: bool = True    # Articulated lab telemetry CRT display
    drawer_units: int = 2               # Under-counter drawer pedestals (1 to 3)

    name: str = "lab_workstation"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 750
