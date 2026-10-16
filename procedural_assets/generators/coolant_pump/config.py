from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class CoolantPumpConfig(BaseAssetConfig):
    """Configuration for Heavy Industrial Coolant Centrifugal Pump Unit."""
    pump_length: float = 0.95
    pump_width: float = 0.55
    pump_height: float = 0.65
    has_pressure_gauge: bool = True     # Dial manometer mounted to the discharge volute
    has_bypass_valve: bool = True       # Handwheel shutoff valve on vertical pipe flange
    motor_fins_count: int = 5           # Longitudinal motor cooling fins
    pump_status: str = "nominal"        # "nominal", "cavitation", "offline"

    name: str = "coolant_pump"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.45
    target_tri_budget: int = 650
