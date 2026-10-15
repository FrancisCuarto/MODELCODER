from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MorgueGurneyConfig(BaseAssetConfig):
    """Configuration for mobile morgue body trolleys, scissor gurneys, and body bag carriers."""
    gurney_type: str = "tray_open"          # "tray_open", "body_bag_closed", "body_bag_ajar"
    width: float = 0.75                     # Frame width in meters
    length: float = 2.05                    # Frame length in meters
    height: float = 0.80                    # Tray top height in meters
    has_scissor_lift: bool = True           # Tubular scissor X-brace elevation frame
    has_push_handles: bool = True           # Ergonomic loop push bars at both ends
    caster_brake_pedals: bool = True        # Foot pedal brakes on caster wheels
    body_silhouette_height: float = 0.22    # Height profile of bagged corpse
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 480
