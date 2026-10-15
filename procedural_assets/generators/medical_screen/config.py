from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MedicalScreenConfig(BaseAssetConfig):
    """Configuration for folding medical privacy screens and quarantine curtain dividers."""
    screen_type: str = "three_panel"        # "three_panel", "four_panel", "single_partition"
    panel_count: int = 3                    # Number of folding panels (1 to 4)
    fold_angle_deg: float = 30.0            # Accordion zig-zag angle in degrees
    panel_width: float = 0.60               # Width of each panel in meters
    panel_height: float = 1.75              # Height from floor in meters
    caster_wheels: bool = True              # Floor caster wheels on leg posts
    curtain_damage: str = "intact"          # "intact", "torn_hanging", "blood_splatter"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 260
