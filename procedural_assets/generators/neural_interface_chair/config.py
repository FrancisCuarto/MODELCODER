from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class NeuralInterfaceChairConfig(BaseAssetConfig):
    """Configuration for Neural Interface Procedure Chair."""
    seat_height: float = 0.52
    backrest_angle: float = 18.0     # Degrees tilted back (0.0 = upright, 45.0 = fully reclined)
    has_sensor_arch: bool = True     # Overhead cognitive sensor crown
    has_restraint_straps: bool = True
    has_side_operator_panel: bool = True
    has_umbilical_cables: bool = True

    name: str = "neural_interface_chair"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.4
    target_tri_budget: int = 750
