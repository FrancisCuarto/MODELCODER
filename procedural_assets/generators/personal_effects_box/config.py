from dataclasses import dataclass, field
from typing import Dict, Any
from ...core.base_config import BaseAssetConfig

@dataclass
class PersonalEffectsBoxConfig(BaseAssetConfig):
    """Configuration for crew personal effects trunk / Pelican-style rugged container."""
    name: str = "personal_effects_box"
    family_id: str = "personal_effects_box"
    category: str = "habitation"
    width: float = 0.44
    depth: float = 0.32
    height: float = 0.22
    box_state: str = "closed"  # closed, open, damaged
    has_latches: bool = True
    has_handle: bool = True
    has_nameplate: bool = True
    has_corner_gussets: bool = True
    wear_level: float = 0.30
    target_tri_budget: int = 280

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "box_state": self.box_state,
            "has_latches": self.has_latches,
            "has_handle": self.has_handle,
            "has_nameplate": self.has_nameplate,
            "has_corner_gussets": self.has_corner_gussets,
        })
        return d
