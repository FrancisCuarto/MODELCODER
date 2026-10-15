from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple, Dict, Any, List
from dataclasses import dataclass, field
import bpy
import bmesh
from .base_config import BaseAssetConfig
from .materials import MaterialManager
from .transform_utils import count_triangles, get_mesh_bounds

TConfig = TypeVar("TConfig", bound=BaseAssetConfig)

@dataclass
class ValidationReport:
    """Validation report containing sanity checks and statistics on generated asset."""
    is_valid: bool
    triangle_count: int
    vertex_count: int
    target_tri_budget: int
    dimensions: Tuple[float, float, float]
    material_names: List[str]
    has_vertex_colors: bool
    has_uv_map: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "triangle_count": self.triangle_count,
            "vertex_count": self.vertex_count,
            "target_tri_budget": self.target_tri_budget,
            "budget_compliance_ratio": round(self.triangle_count / max(1, self.target_tri_budget), 2),
            "dimensions": {
                "x": round(self.dimensions[0], 4),
                "y": round(self.dimensions[1], 4),
                "z": round(self.dimensions[2], 4)
            },
            "material_names": self.material_names,
            "has_vertex_colors": self.has_vertex_colors,
            "has_uv_map": self.has_uv_map,
            "errors": self.errors,
            "warnings": self.warnings
        }

class BaseAssetGenerator(ABC, Generic[TConfig]):
    """Abstract base class for all procedural asset generators."""

    def __init__(self, material_manager: MaterialManager = None):
        self.material_manager = material_manager or MaterialManager()

    def get_material_manager(self, config: TConfig) -> MaterialManager:
        """Create or configure MaterialManager using config's palette and wear settings."""
        palette = getattr(config, "palette_name", getattr(config, "style_palette", "industrial_hazard"))
        wear = getattr(config, "wear_level", 0.5)
        emission_mult = getattr(config, "emission_scale", 1.0)
        seed = getattr(config, "seed", 42)
        mat_mgr = MaterialManager(
            palette_name=palette,
            wear_level=wear,
            seed=seed,
            emission_multiplier=emission_mult
        )
        from .mesh_builder import MeshBuilder
        MeshBuilder.set_active_material_manager(mat_mgr)
        return mat_mgr

    @staticmethod
    def clean_context():
        """Ensure clean Blender state before generation."""
        # Deselect all
        for obj in bpy.data.objects:
            obj.select_set(False)

    @abstractmethod
    def generate(self, config: TConfig) -> bpy.types.Object:
        """Procedurally generate mesh geometry and return a Blender object."""
        pass

    @staticmethod
    def create_mesh_object(name: str) -> Tuple[bpy.types.Object, bmesh.types.BMesh]:
        """Create a new mesh object linked to context collection and an active BMesh with UVMap and Col layers."""
        mesh_name = f"{name}_mesh"
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
        if mesh_name in bpy.data.meshes:
            bpy.data.meshes.remove(bpy.data.meshes[mesh_name], do_unlink=True)
        mesh = bpy.data.meshes.new(name=mesh_name)
        obj = bpy.data.objects.new(name=name, object_data=mesh)
        bpy.context.collection.objects.link(obj)
        bm = bmesh.new()
        # Initialize standard UV and Color layers so all builder operations inherit them
        bm.loops.layers.uv.new("UVMap")
        bm.loops.layers.color.new("Col")
        return obj, bm

    @classmethod
    def ensure_faces_have_uvs_and_colors(cls, bm: bmesh.types.BMesh, obj: bpy.types.Object):
        """Audit all faces in BMesh to ensure none have missing/zero UVs or missing vertex colors."""
        from .mesh_builder import MeshBuilder
        uv_layer = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.active
        if not uv_layer:
            uv_layer = bm.loops.layers.uv.new("UVMap")

        col_layer = bm.loops.layers.color.get("Col") or bm.loops.layers.color.get("Color") or bm.loops.layers.color.active
        if not col_layer:
            col_layer = bm.loops.layers.color.new("Col")

        for f in bm.faces:
            loops = f.loops
            if not loops:
                continue

            # Check if UVs are unmapped (all 0, 0)
            uvs = [l[uv_layer].uv for l in loops]
            is_unmapped = all(abs(u) < 1e-5 and abs(v) < 1e-5 for u, v in uvs)
            if is_unmapped:
                rect = MeshBuilder.resolve_uv_rect(f.material_index)
                if len(loops) == 4:
                    MeshBuilder.apply_box_face_uv(f, uv_layer, rect)
                else:
                    MeshBuilder.apply_face_uv_rect(f, uv_layer, rect)

            # Check if vertex colors are unassigned or black
            colors = [l[col_layer] for l in loops]
            if all(c[3] < 0.05 for c in colors):
                rgba = (0.5, 0.5, 0.5, 1.0)
                if MeshBuilder.active_material_manager and hasattr(MeshBuilder.active_material_manager, "get_key_by_index"):
                    mat_key = MeshBuilder.active_material_manager.get_key_by_index(f.material_index)
                    if mat_key:
                        rgba = MeshBuilder.active_material_manager.get_rgba(mat_key)
                for l in loops:
                    l[col_layer] = rgba

    @classmethod
    def finalize_mesh(cls, obj: bpy.types.Object, bm: bmesh.types.BMesh):
        """Write BMesh to object's mesh data and ensure vertex color attribute and UV layer."""
        cls.ensure_faces_have_uvs_and_colors(bm, obj)

        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        # Ensure vertex color attribute and UV map exist on Blender mesh
        if len(obj.data.color_attributes) == 0:
            obj.data.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
        if len(obj.data.uv_layers) == 0:
            obj.data.uv_layers.new(name="UVMap")

        MaterialManager.compact_materials(obj)

    def validate(self, obj: bpy.types.Object, config: TConfig) -> ValidationReport:
        """Verify geometry exists, adheres to budget, and matches configuration parameters."""
        errors = []
        warnings = []

        if not obj or not obj.data or not isinstance(obj.data, bpy.types.Mesh):
            return ValidationReport(
                is_valid=False,
                triangle_count=0,
                vertex_count=0,
                target_tri_budget=config.target_tri_budget,
                dimensions=(0, 0, 0),
                material_names=[],
                has_vertex_colors=False,
                has_uv_map=False,
                errors=["Object is None or does not contain valid Mesh data"]
            )

        MaterialManager.compact_materials(obj)

        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        tri_count = count_triangles(bm)
        vert_count = len(bm.verts)
        _, _, dims = get_mesh_bounds(bm)
        bm.free()

        # Check vertex & tri existence
        if vert_count == 0 or tri_count == 0:
            errors.append(f"Mesh has empty geometry: {vert_count} vertices, {tri_count} triangles")

        # Triangle budget check: allow 15% tolerance before flagging warning
        max_budget = int(config.target_tri_budget * 1.15)
        if tri_count > max_budget:
            warnings.append(
                f"Triangle count ({tri_count}) exceeded target budget ({config.target_tri_budget}) by more than 15%"
            )

        # Materials check
        mat_names = [slot.material.name for slot in obj.material_slots if slot.material]
        if not mat_names:
            warnings.append("No materials assigned to mesh")

        # Vertex colors check
        has_color_attr = len(mesh.color_attributes) > 0
        if not has_color_attr:
            warnings.append("Mesh does not contain vertex color attributes")

        # UV layers check
        has_uv_layer = len(mesh.uv_layers) > 0
        if not has_uv_layer:
            errors.append("Mesh does not contain a UV layer (UVMap)")

        is_valid = len(errors) == 0

        return ValidationReport(
            is_valid=is_valid,
            triangle_count=tri_count,
            vertex_count=vert_count,
            target_tri_budget=config.target_tri_budget,
            dimensions=(dims.x, dims.y, dims.z),
            material_names=mat_names,
            has_vertex_colors=has_color_attr,
            has_uv_map=has_uv_layer,
            errors=errors,
            warnings=warnings
        )

BaseGenerator = BaseAssetGenerator
__all__ = ["BaseAssetGenerator", "BaseGenerator", "ValidationReport"]
