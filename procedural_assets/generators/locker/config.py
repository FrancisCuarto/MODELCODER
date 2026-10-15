from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class LockerConfig(BaseAssetConfig):
    """Configuration for crew lockers, benches and technical storage cabinets."""
    columns: int = 2  # 1 to 4 locker doors in bank
    column_width: float = 0.42
    height: float = 1.90
    depth: float = 0.50

    door_state: str = "all_closed"  # "all_closed", "one_open", "damaged_forced"
    has_integrated_bench: bool = True  # Station locker bench in front
    has_top_hat_shelf: bool = True  # Helmet shelf compartment
    has_louvers: bool = True
    has_number_plates: bool = True

    name: str = "crew_lockers"
    target_tri_budget: int = 400
