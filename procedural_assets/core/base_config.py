from dataclasses import dataclass, asdict, field
from typing import Any, Dict
import json

@dataclass
class BaseAssetConfig:
    """Base configuration for any procedural asset."""
    seed: int = 42
    target_tri_budget: int = 450
    name: str = "asset"
    wear_level: float = 0.5  # 0.0 = mint factory, 1.0 = ruined/heavy rust & grime
    add_collision_mesh: bool = False  # Generate Godot 4 collision shape
    collision_type: str = "box"  # "box", "convex_hull", "none"
    collision_suffix: str = "-convcolonly"  # "-convcolonly", "-colonly", "-convcol", "-col"
    pivot_rule: str = "floor_center"  # "floor_center", "center", "wall_back", "keep"
    export_subcomponents: bool = False  # When True, keeps subcomponents as separate child nodes
    palette_name: str = "industrial_hazard"  # industrial_hazard, medbay_clean, command_bridge, habitation_worn, derelict_decay
    emission_scale: float = 1.0  # Multiplier for screen and indicator light emission intensity
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert configuration to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create configuration instance from dictionary."""
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)
