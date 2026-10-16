from dataclasses import dataclass
from ...core.base_config import BaseAssetConfig

@dataclass
class SampleAnalyzerConfig(BaseAssetConfig):
    """Configuration for Benchtop Automated Sample Spectrometer / Analyzer."""
    width: float = 0.55
    depth: float = 0.60
    height: float = 0.38
    tray_extended: float = 0.0          # 0.0 = sealed internal chamber, 0.15 = ejected sample rack tray
    analyzer_state: str = "processing"   # "idle", "processing", "alarm", "error"
    has_barcode_scanner: bool = True     # Side optical barcode wand holster
    has_thermal_printer: bool = True     # Top slot thermal result tape dispenser

    name: str = "sample_analyzer"
    palette_name: str = "medbay_clean"
    wear_level: float = 0.30
    target_tri_budget: int = 550
