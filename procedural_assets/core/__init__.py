from .base_config import BaseAssetConfig
from .manifest import (
    GeneratorManifest,
    ParameterDef,
    AuthorDef,
    PresetDef,
    find_manifest_for_family,
    discover_all_manifests,
)

try:
    from .base_generator import BaseAssetGenerator, ValidationReport
    from .materials import MaterialManager, MaterialDef
    from .mesh_builder import MeshBuilder
    from .transform_utils import count_triangles, get_mesh_bounds, generate_catenary_cable_points
except (ImportError, ModuleNotFoundError):
    BaseAssetGenerator = None  # type: ignore
    ValidationReport = None  # type: ignore
    MaterialManager = None  # type: ignore
    MaterialDef = None  # type: ignore
    MeshBuilder = None  # type: ignore
    count_triangles = None  # type: ignore
    get_mesh_bounds = None  # type: ignore
    generate_catenary_cable_points = None  # type: ignore


__all__ = [
    "BaseAssetConfig",
    "BaseAssetGenerator",
    "ValidationReport",
    "MaterialManager",
    "MaterialDef",
    "MeshBuilder",
    "count_triangles",
    "get_mesh_bounds",
    "generate_catenary_cable_points",
    "GeneratorManifest",
    "ParameterDef",
    "AuthorDef",
    "PresetDef",
    "find_manifest_for_family",
    "discover_all_manifests",
]
