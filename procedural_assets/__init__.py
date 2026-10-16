"""
Procedural Asset Generator for Video Games (PSX Low-Poly Aesthetic)
Targeted for "Below Nominal" - Retrofuturistic Industrial Survival Horror.
"""

try:
    from .core.base_config import BaseAssetConfig
    from .core.base_generator import BaseAssetGenerator, ValidationReport
    from .core.materials import MaterialManager
    from .generators.electrical_panel.config import ElectricalPanelConfig
    from .generators.electrical_panel.generator import ElectricalPanelGenerator
    from .export.glb_exporter import GLBExporter
except (ImportError, ModuleNotFoundError):
    BaseAssetConfig = None  # type: ignore
    BaseAssetGenerator = None  # type: ignore
    ValidationReport = None  # type: ignore
    MaterialManager = None  # type: ignore
    ElectricalPanelConfig = None  # type: ignore
    ElectricalPanelGenerator = None  # type: ignore
    GLBExporter = None  # type: ignore

__version__ = "0.1.0"

__all__ = [
    "BaseAssetConfig",
    "BaseAssetGenerator",
    "ValidationReport",
    "MaterialManager",
    "ElectricalPanelConfig",
    "ElectricalPanelGenerator",
    "GLBExporter",
]

