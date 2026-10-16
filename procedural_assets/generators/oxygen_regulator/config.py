from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class OxygenRegulatorConfig(BaseAssetConfig):
    """Configuration for Oxygen Regulator mural pressure manifold."""
    width: float = 0.45
    height: float = 0.55
    gauge_count: int = 2               # 1 to 3 circular gauges
    has_brass_valves: bool = True
    has_emergency_shutoff: bool = True
    has_flow_meter: bool = True

    name: str = "oxygen_regulator"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.4
    target_tri_budget: int = 420
