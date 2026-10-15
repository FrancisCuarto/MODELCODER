from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class BridgeConsoleDeskConfig(BaseAssetConfig):
    """Configuration for ship bridge command consoles, navigation horseshoe desks, and reactor control banks."""
    console_shape: str = "u_shaped"          # "u_shaped", "crescent_arc", "dual_operator"
    width: float = 2.20                     # Overall console width in meters
    depth: float = 1.60                     # Overall console depth in meters
    height: float = 1.05                    # Main console canopy height in meters
    crt_count: int = 3                      # Number of recessed CRT monitor banks (1 to 4)
    has_toggle_guards: bool = True          # Flip-up missile covers over critical breakers
    has_microphone_stalk: bool = True       # Flexible gooseneck comms stalk
    chair_included: bool = True             # Central integrated heavy pilot swivel chair
    screen_color: str = "green"             # "green", "amber"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 380
