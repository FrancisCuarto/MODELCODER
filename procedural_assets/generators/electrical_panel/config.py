from dataclasses import dataclass
from typing import Optional
from ...core.base_config import BaseAssetConfig

@dataclass
class ElectricalPanelConfig(BaseAssetConfig):
    """Configuration specific to the Industrial Electrical Panel asset family."""
    # Physical dimensions in meters (calibrated for 1st person scale)
    width: float = 0.70
    height: float = 0.90
    depth: float = 0.22
    wall_thickness: float = 0.035

    # Features & Components
    has_crt: bool = True
    crt_size_ratio: float = 0.38
    crt_phosphor_color: str = "green"  # "green" or "amber"
    crt_bulge: float = 0.025

    button_rows: int = 2
    button_cols: int = 3
    switch_count: int = 2
    indicator_count: int = 3
    cable_count: int = 2

    has_knife_switch: bool = False  # Heavy dual-pole knife breaker
    door_ajar: bool = False  # Swung open maintenance door
    door_open_angle: float = 35.0  # Degrees swung open (0 to 90)
    has_digital_readout: bool = True  # Segmented LED digital readout
    has_side_vents: bool = True
    has_mounting_flanges: bool = True
    style_palette: str = "industrial_hazard"

    # Default asset naming and budget
    name: str = "electrical_panel"
    target_tri_budget: int = 450
