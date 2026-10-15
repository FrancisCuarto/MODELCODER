"""
Procedural Asset Generator for Video Games (PSX Low-Poly Aesthetic)
Targeted for "Below Nominal" - Retrofuturistic Industrial Survival Horror.
"""

from .core.base_config import BaseAssetConfig
from .core.base_generator import BaseAssetGenerator, ValidationReport
from .core.materials import MaterialManager
from .generators.electrical_panel.config import ElectricalPanelConfig
from .generators.electrical_panel.generator import ElectricalPanelGenerator
from .export.glb_exporter import GLBExporter

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
