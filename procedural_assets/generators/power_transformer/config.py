from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class PowerTransformerConfig(BaseAssetConfig):
    """Configuration for Heavy Electrical Power Substation Transformer."""
    transformer_width: float = 1.1
    transformer_depth: float = 0.85
    transformer_height: float = 1.45
    insulator_count: int = 3             # 2 to 4 high-voltage ribbed ceramic bushings
    cooling_radiators_sides: bool = True # Heat-dissipation oil radiator fin banks on sides
    has_expansion_tank: bool = True      # Top conservator oil reservoir cylinder

    name: str = "power_transformer"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.50
    target_tri_budget: int = 680
