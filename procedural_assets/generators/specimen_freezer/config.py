from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SpecimenFreezerConfig(BaseAssetConfig):
    """Configuration for Ultra-Low Temperature Specimen Cryo-Freezer (-80°C)."""
    freezer_width: float = 0.9
    freezer_depth: float = 0.8
    freezer_height: float = 1.9
    door_open_angle: float = 0.0          # 0.0 = sealed vacuum latch, 90.0 = fully open
    tray_count: int = 4                   # 3 to 5 internal slide-out cryo racks
    temperature_celsius: float = -80.0    # Display temp readout (-86 to +20)
    has_alarm_beacon: bool = False        # Flashing red beacon on top if cold chain breached
    has_frost_buildup: bool = True        # Frost/condensation around seals and window
    has_window: bool = True               # Small triple-pane inspection window

    name: str = "specimen_freezer"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 720
