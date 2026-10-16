from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class QuarantineBedConfig(BaseAssetConfig):
    """Configuration for Clinical Isolation Quarantine Bed."""
    bed_length: float = 2.1
    bed_width: float = 0.95
    bed_height: float = 0.85
    headrest_angle: float = 15.0      # 0.0 to 45.0 degrees raised
    rails_raised: bool = True          # Safety isolation side rails raised or lowered
    has_iv_pole: bool = True           # Tall IV fluid pole attached to bedframe
    has_restraint_straps: bool = True  # Heavy containment straps across mattress
    has_patient_bulk: bool = False     # Covered sheet silhouette under sterile draping
    has_monitor_arm: bool = True       # Swivel vitals display terminal on articulated arm

    name: str = "quarantine_bed"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.35
    target_tri_budget: int = 750
