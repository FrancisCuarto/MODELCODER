from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class MessTableConfig(BaseAssetConfig):
    """Configuration for crew canteen tables with bolted-to-floor swivel stools."""
    table_type: str = "bolted_stools_4"      # "bolted_stools_4", "bolted_stools_6", "free_standing_bench"
    stool_count: int = 4                    # Number of attached stools (2, 4, 6)
    table_width: float = 0.90               # Tabletop width in meters
    table_length: float = 1.80              # Tabletop length in meters
    table_height: float = 0.78              # Surface height in meters
    stool_swing_state: str = "random_pulled"# "all_tucked", "random_pulled", "scattered"
    has_mess_trays: bool = True             # Abandoned food trays and tin cups
    has_floor_bolts: bool = True            # Heavy floor anchoring flanges
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 450
