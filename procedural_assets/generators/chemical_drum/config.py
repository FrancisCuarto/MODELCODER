from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ChemicalDrumConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial 55-Gallon Chemical Storage Drum."""
    diameter: float = 0.58
    height: float = 0.90
    rib_count: int = 2                   # 1 to 3 rolled rolling hoops / reinforcement ribs
    has_bung_caps: bool = True           # Threaded 2" and 3/4" bung plugs with hex heads
    has_spill_residue: bool = False      # Chemical staining / dried corrosive residue ring
    hazard_type: str = "corrosive"       # "corrosive", "toxic", "flammable", "coolant"

    name: str = "chemical_drum"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 420
