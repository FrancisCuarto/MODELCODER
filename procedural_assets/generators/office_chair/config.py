from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OfficeChairConfig(BaseAssetConfig):
    """
    Configuration for Industrial Swivel Task & Command Chairs.
    Survival horror aesthetics: worn vinyl cushions, pneumatic cylinders, broken armrest variants.
    """
    # Seat cushion dimensions
    seat_width: float = 0.52
    seat_depth: float = 0.50
    seat_height: float = 0.48
    cushion_thickness: float = 0.08

    # Backrest styling
    backrest_style: str = "mid_back"  # "mid_back", "high_back_headrest", "low_back"
    backrest_height: float = 0.45
    backrest_tilt: float = 8.0  # degrees tilted back

    # Base & running gear
    base_style: str = "five_star_casters"  # "five_star_casters", "four_leg_tubular", "pedestal_bolted"
    spoke_count: int = 5
    base_radius: float = 0.32

    # Armrests (with environmental storytelling options)
    armrest_style: str = "both"  # "both", "one_broken", "none"
    armrest_height: float = 0.22

    # Material & aesthetic
    upholstery_color: str = "dark_charcoal"  # "dark_charcoal", "emergency_red", "industrial_blue"
    name: str = "office_chair"
    target_tri_budget: int = 380
    wear_level: float = 0.65
