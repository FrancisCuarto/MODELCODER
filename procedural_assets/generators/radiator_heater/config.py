from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class RadiatorHeaterConfig(BaseAssetConfig):
    """Configuration for industrial space radiators, convector blowers, and thermal heat exchangers."""
    heater_type: str = "wall_radiator_fins"  # "wall_radiator_fins", "convector_blower", "space_tower_heater"
    width: float = 0.85                      # Width in meters
    height: float = 0.70                     # Height in meters
    depth: float = 0.22                      # Depth in meters
    fin_count: int = 8                       # Number of radiator fin plates (4-14)
    is_operational: bool = True              # Glow from heating elements through vents
    has_thermostat_dial: bool = True         # Brass/plastic control knob
    has_steam_pipe: bool = True              # Feed pipe with red shutoff handwheel
    damage_state: str = "intact"             # "intact", "battered_bent_fins", "leaking_burst"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
