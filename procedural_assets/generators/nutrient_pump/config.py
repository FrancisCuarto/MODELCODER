from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class NutrientPumpConfig(BaseAssetConfig):
    """Configuration for botanical nutrient dosing pump with inline filter."""
    name: str = "nutrient_pump"
    family_id: str = "nutrient_pump"
    category: str = "hydroponics"
    pump_size: float = 0.45
    motor_type: str = "electric_finned"  # electric_finned, compact_servo
    has_filter_canister: bool = True
    has_pressure_dial: bool = True
    pump_state: str = "active"          # active, clogged, service_off
    wear_level: float = 0.35
    target_tri_budget: int = 300

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "pump_size": self.pump_size,
            "motor_type": self.motor_type,
            "has_filter_canister": self.has_filter_canister,
            "has_pressure_dial": self.has_pressure_dial,
            "pump_state": self.pump_state,
        })
        return d
