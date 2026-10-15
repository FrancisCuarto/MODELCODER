from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class HydroponicTrayBedConfig(BaseAssetConfig):
    """Configuration for botanical hydroponics trays, life support algae cultures, and growth racks."""
    bed_type: str = "single_tier"           # "single_tier", "stacked_dual_tier", "quarantine_specimen_tank"
    width: float = 1.40                     # Bed width in meters
    depth: float = 0.80                     # Bed depth in meters
    height: float = 1.20                    # Total height including overhead UV lamp arch in meters
    plant_state: str = "healthy_green"      # "healthy_green", "withered_dead", "mutated_spores"
    uv_light_state: str = "on_violet"       # "on_violet", "flickering", "off"
    fluid_pipes: bool = True                # Nutrient solution recirculating pipe manifold
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 480
