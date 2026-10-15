from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OfficeDoorConfig(BaseAssetConfig):
    """Configuration for glazed office, laboratory, and clinic doors with reinforced glass."""
    door_style: str = "single_swing"        # "single_swing", "double_swing", "sliding_pocket"
    glass_type: str = "wired_safety_glass"  # "wired_safety_glass", "clear_tinted", "frosted_privacy"
    width: float = 1.20                     # Overall frame width in meters
    height: float = 2.40                    # Overall frame height in meters
    frame_depth: float = 0.22               # Wall jamb thickness in meters
    open_angle_deg: float = 0.0             # 0.0 = closed, 20.0 = ajar, 85.0 = open
    glass_damage: str = "intact"            # "intact", "cracked_spiderweb", "shattered_missing"
    handle_type: str = "horizontal_push_bar"# "horizontal_push_bar", "industrial_lever", "recessed_pull"
    has_kickplate: bool = True              # Heavy steel bottom kickplate
    has_transom: bool = False               # Upper observation transom window above door header
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 420
