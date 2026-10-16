from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CargoPalletConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial 4-Way Entry Logistics Cargo Pallet."""
    length: float = 1.20
    width: float = 1.00
    height: float = 0.16
    deck_style: str = "slotted_deck"     # "slotted_deck", "solid_flat", "reinforced_steel"
    has_cargo_payload: bool = False      # Stacked ration supply crates strapped onto deck
    has_strap_down: bool = True          # High-tensile ratchet tie-down straps with buckles
    pallet_condition: str = "nominal"    # "nominal", "damaged_corner", "chemical_stained"

    name: str = "cargo_pallet"
    pivot_rule: str = "floor_center"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.50
    target_tri_budget: int = 380
