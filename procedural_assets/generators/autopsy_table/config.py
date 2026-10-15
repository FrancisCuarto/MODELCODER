from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class AutopsyTableConfig(BaseAssetConfig):
    """Configuration for surgical autopsy, dissection slabs, and quarantine examination tables."""
    table_type: str = "standard_autopsy"    # "standard_autopsy", "dissection_station", "quarantine_slab"
    width: float = 0.90                     # Table width in meters
    length: float = 2.10                    # Table length in meters
    height: float = 0.85                    # Table surface height in meters
    drainage_channel: bool = True           # Perimeter fluid trough and central drain
    overhead_lamp: bool = True              # Articulated surgical examination spotlight
    restraint_straps: str = "none"          # "none", "buckled", "torn"
    fluid_stain: bool = True                # Dried fluid staining and oxidation
    has_instrument_tray: bool = False       # Swivel cantilever surgical tray with bone saw & tools
    specimen_jar_count: int = 0             # Glass quarantine specimen jars with formaldehyde (0 to 3)
    palette_name: str = "industrial_hazard"
    target_tri_budget: int = 420
