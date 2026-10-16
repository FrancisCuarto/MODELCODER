"""
ModelCoder Palette and Material Compatibility Layer for Community Generators.
"""

from typing import Optional
from ..core.materials import MaterialManager

_shared_manager: Optional[MaterialManager] = None

def get_or_create_material(category_or_role: str, sub_role: Optional[str] = None, palette_name: str = "industrial_hazard"):
    """
    Helper function for generators to quickly retrieve PSX procedural materials.
    """
    global _shared_manager
    if _shared_manager is None or _shared_manager.palette_name != palette_name:
        try:
            _shared_manager = MaterialManager(palette_name=palette_name)
        except Exception:
            _shared_manager = None

    if _shared_manager:
        try:
            return _shared_manager.get_or_create_material(category_or_role)
        except Exception:
            pass
    return None
