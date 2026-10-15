from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class LightFixtureConfig(BaseAssetConfig):
    """
    Configuration for Europa station industrial luminaires, fluorescent tubes, and emergency beacons.
    Supports flickering/dead tubes, dangling electrical conduit, and dented protective cages.
    """
    fixture_type: str = "fluorescent_troffer"  # "fluorescent_troffer", "bulkhead_cage", "emergency_beacon", "pendant_industrial"
    length: float = 1.20
    width: float = 0.28
    depth: float = 0.10

    # Lamp state and tubes
    tube_count: int = 2
    lighting_state: str = "both_working"  # "both_working", "flickering_one_dead", "completely_dead", "emergency_red"

    # Protection & environmental damage
    has_wire_guard: bool = True  # Steel protective wire cage
    has_dangling_wire: bool = False  # Dangling power cord
    has_bent_cage: bool = False

    name: str = "light_fixture"
    target_tri_budget: int = 340
    wear_level: float = 0.65
