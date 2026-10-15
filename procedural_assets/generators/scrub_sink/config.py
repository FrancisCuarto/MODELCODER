from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ScrubSinkConfig(BaseAssetConfig):
    """Configuration for surgical scrub sinks, decontamination wash basins, and hospital sinks."""
    sink_type: str = "surgical_single"       # "surgical_single", "double_bay", "decon_basin"
    width: float = 0.70                     # Basin width in meters
    depth: float = 0.55                     # Basin depth in meters
    height: float = 1.15                    # Backsplash top height in meters
    faucet_type: str = "gooseneck_sensor"   # "gooseneck_sensor", "elbow_blade_levers", "foot_pedal_valves"
    has_soap_dispenser: bool = True         # Wall mounted surgical antiseptic dispenser
    has_splash_mirror: bool = True          # Inset stainless steel polished reflector plate
    drain_state: str = "clean"              # "clean", "blood_stained"
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 260
