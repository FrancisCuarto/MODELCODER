from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class BatteryBankConfig(BaseAssetConfig):
    """Configuration for Industrial Emergency Energy Accumulator Battery Bank."""
    rack_width: float = 1.30
    rack_depth: float = 0.65
    rack_height: float = 1.65
    tier_count: int = 3                  # 2 to 4 horizontal shelf tiers
    batteries_per_tier: int = 4          # 3 to 5 heavy industrial battery cells per tier
    has_busbars: bool = True             # Thick copper interconnect busbar strips between poles
    has_charge_monitor: bool = True      # Top-mounted digital telemetry charge monitor
    charge_state: str = "nominal"        # "nominal", "discharging", "depleted", "alarm"

    name: str = "battery_bank"
    palette_name: str = "industrial_hazard"
    wear_level: float = 0.40
    target_tri_budget: int = 720
