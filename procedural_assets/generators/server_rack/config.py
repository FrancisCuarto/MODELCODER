from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class ServerRackConfig(BaseAssetConfig):
    """Configuration for consciousness memory storage and server racks."""
    rack_type: str = "consciousness_bank"  # "consciousness_bank", "telemetry_server", "cryo_cooling_rack"
    width: float = 0.80
    height: float = 2.00
    depth: float = 0.85

    blade_units: int = 6
    cartridge_occupancy: float = 0.80  # 0.0 = all slots empty, 1.0 = fully populated
    cooling_system: str = "cooling_pipes"  # "cooling_pipes", "louver_vents", "mesh_grill"
    has_service_terminal: bool = True  # Pull-out 1U monitor & keyboard tray
    has_cable_conduit: bool = True
    has_side_louvers: bool = True

    name: str = "consciousness_server_rack"
    target_tri_budget: int = 500
