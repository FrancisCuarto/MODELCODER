import os
import math
from typing import Tuple, Dict, Any, List, Optional
import bpy
import bmesh
import mathutils

from ..core.base_generator import BaseAssetGenerator, ValidationReport
from ..core.base_config import BaseAssetConfig
from ..core.materials import MaterialManager
from ..core.transform_utils import get_mesh_bounds
from .metadata_sidecar import save_metadata_sidecar
from .export_report import generate_export_report
from .godot_validator import validate_glb_with_godot, is_godot_available

class ExportResult(tuple):
    """
    Tuple representing export results: (glb_filepath, metadata_json_path).
    Provides backward-compatible 2-tuple unpacking while exposing extra report paths as attributes.
    """
    def __new__(cls, glb_path: str, json_path: str, report_json: str = "", report_md: str = ""):
        return super().__new__(cls, (glb_path, json_path))

    def __init__(self, glb_path: str, json_path: str, report_json: str = "", report_md: str = ""):
        self.glb_path = glb_path
        self.json_path = json_path
        self.report_json_path = report_json
        self.report_md_path = report_md

class GLBExporter:
    """
    Production-grade glTF/GLB export pipeline for Below Nominal assets targeted at Godot 4.
    Normalizes scale, orientation, transforms, pivots, normals, multi-object hierarchies,
    Godot 4 collision nodes, socket empties, and validates via headless Godot execution.
    """

    @staticmethod
    def normalize_mesh_normals(obj: bpy.types.Object):
        """Force authentic PS1 low-poly flat shading and recalculate outward-facing normals."""
        if not obj or not obj.data or not isinstance(obj.data, bpy.types.Mesh):
            return

        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Recalculate outward normals
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

        # Ensure flat shading on all faces (PS1 aesthetic)
        for face in bm.faces:
            face.smooth = False

        bm.to_mesh(mesh)
        bm.free()

        # In Blender mesh polygons, ensure use_smooth is False
        for poly in mesh.polygons:
            poly.use_smooth = False

        mesh.update()

    @staticmethod
    def normalize_transforms(objects: List[bpy.types.Object]):
        """
        Bake scale, rotation, and translation into mesh geometry so that all object
        transform matrices are strictly identity matrices:
        Location = (0,0,0), Rotation = (0,0,0), Scale = (1,1,1).
        """
        for o in objects:
            if o.type == 'MESH' and o.data:
                # Apply transforms directly via matrix multiplication on vertices
                matrix = o.matrix_basis.copy()
                if matrix != mathutils.Matrix.Identity(4):
                    o.data.transform(matrix)
                    o.matrix_basis = mathutils.Matrix.Identity(4)
                    o.data.update()

    @staticmethod
    def normalize_pivot(
        root_obj: bpy.types.Object,
        rule: str = "floor_center"
    ) -> Tuple[mathutils.Vector, mathutils.Vector, mathutils.Vector, mathutils.Vector]:
        """
        Calculates total bounds across the visual object and offsets vertices so that:
        - 'floor_center' (default for standing furniture/props): bottom Z = 0.0, centered in X and Y.
        - 'center': centered in X, Y, Z.
        - 'wall_back': back plane Y = 0.0, centered in X, bottom Z = 0.0.
        - 'keep': no offset applied.

        Returns: (min_co, max_co, dimensions, applied_offset)
        """
        if not root_obj or not root_obj.data:
            zero = mathutils.Vector((0, 0, 0))
            return zero, zero, zero, zero

        # Collect all visual mesh vertices in root object's local space
        min_x = float('inf')
        min_y = float('inf')
        min_z = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        max_z = float('-inf')

        for v in root_obj.data.vertices:
            min_x = min(min_x, v.co.x)
            min_y = min(min_y, v.co.y)
            min_z = min(min_z, v.co.z)
            max_x = max(max_x, v.co.x)
            max_y = max(max_y, v.co.y)
            max_z = max(max_z, v.co.z)

        min_co = mathutils.Vector((min_x, min_y, min_z))
        max_co = mathutils.Vector((max_x, max_y, max_z))
        dims = max_co - min_co

        # Compute translation delta according to rule
        delta = mathutils.Vector((0.0, 0.0, 0.0))
        if rule == "floor_center":
            delta.x = - (min_x + max_x) / 2.0
            delta.y = - (min_y + max_y) / 2.0
            delta.z = - min_z
        elif rule == "center":
            delta.x = - (min_x + max_x) / 2.0
            delta.y = - (min_y + max_y) / 2.0
            delta.z = - (min_z + max_z) / 2.0
        elif rule == "wall_back":
            delta.x = - (min_x + max_x) / 2.0
            delta.y = - min_y
            delta.z = - min_z
        elif rule == "keep":
            pass

        if delta.length > 0.0001:
            trans_mat = mathutils.Matrix.Translation(delta)
            root_obj.data.transform(trans_mat)
            root_obj.data.update()

            # Update bounds post-translation
            min_co += delta
            max_co += delta

        return min_co, max_co, dims, delta

    @staticmethod
    def create_collision_shape(
        obj: bpy.types.Object,
        config: BaseAssetConfig,
        min_co: mathutils.Vector,
        max_co: mathutils.Vector,
        dims: mathutils.Vector
    ) -> Optional[bpy.types.Object]:
        """
        Creates an isolated collision object formatted with Godot 4 import suffixes:
        - -convcolonly: Godot converts to StaticBody3D with ConvexPolygonShape3D and removes visual mesh.
        - -colonly: Godot converts to StaticBody3D with ConcavePolygonShape3D (trimesh) and removes visual mesh.
        """
        if not getattr(config, "add_collision_mesh", False):
            return None

        suffix = getattr(config, "collision_suffix", "-convcolonly")
        col_type = getattr(config, "collision_type", "box")

        col_name = f"{obj.name}{suffix}"
        col_mesh = bpy.data.meshes.new(f"{col_name}_mesh")
        col_obj = bpy.data.objects.new(col_name, col_mesh)
        bpy.context.collection.objects.link(col_obj)
        col_obj.parent = obj

        bm_c = bmesh.new()

        if col_type == "convex_hull" and obj.data:
            # Generate exact convex hull from visual mesh vertices
            bm_src = bmesh.new()
            bm_src.from_mesh(obj.data)
            hull_res = bmesh.ops.convex_hull(bm_c, input=bm_src.verts)
            # Free unused elements from hull operation
            geom_unused = hull_res.get("geom_unused", [])
            for elem in geom_unused:
                if isinstance(elem, bmesh.types.BMVert) and elem.is_valid:
                    bm_c.verts.remove(elem)
            bm_src.free()
        else:
            # Default: Fitted bounding box
            center = (min_co + max_co) / 2.0
            size_x = max(0.05, dims.x)
            size_y = max(0.05, dims.y)
            size_z = max(0.05, dims.z)

            bmesh.ops.create_cube(bm_c, size=1.0)
            for v in bm_c.verts:
                v.co.x = center.x + (v.co.x * size_x)
                v.co.y = center.y + (v.co.y * size_y)
                v.co.z = center.z + (v.co.z * size_z)

        # Ensure flat shading and clean outward normals for collision
        bmesh.ops.recalc_face_normals(bm_c, faces=bm_c.faces)
        for f in bm_c.faces:
            f.smooth = False

        bm_c.to_mesh(col_mesh)
        bm_c.free()
        col_mesh.update()

        return col_obj

    @staticmethod
    def create_socket_nodes(
        obj: bpy.types.Object,
        sockets: List[Dict[str, Any]],
        pivot_delta: mathutils.Vector
    ) -> List[bpy.types.Object]:
        """
        Creates Blender Empty objects for each socket under the root object.
        Godot 4 glTF importer automatically imports empties as native Node3D attachment points!
        """
        empty_objs = []
        for s in sockets:
            s_name = s.get("name", "socket")
            empty = bpy.data.objects.new(s_name, None)
            empty.empty_display_type = 'PLAIN_AXES'
            empty.empty_display_size = 0.1

            raw_pos = s.get("position", [0.0, 0.0, 0.0])
            pos_vec = mathutils.Vector((raw_pos[0], raw_pos[1], raw_pos[2]))
            pos_vec += pivot_delta

            empty.location = pos_vec
            bpy.context.collection.objects.link(empty)
            empty.parent = obj
            empty_objs.append(empty)

        return empty_objs

    @classmethod
    def ensure_mesh_uvs_and_materials(cls, obj: bpy.types.Object):
        """Audit mesh prior to glTF export to guarantee UVMap exists and all polygons have valid UV coordinates."""
        if not obj or obj.type != 'MESH' or not obj.data:
            return

        mesh = obj.data
        if not mesh.polygons:
            return

        # Ensure UVMap exists
        uv_layer = mesh.uv_layers.get("UVMap")
        if not uv_layer:
            uv_layer = mesh.uv_layers.active
        if not uv_layer:
            uv_layer = mesh.uv_layers.new(name="UVMap")

        # Set active render
        uv_layer.active_render = True
        mesh.uv_layers.active = uv_layer

        # Ensure Col color attribute exists
        if len(mesh.color_attributes) == 0:
            mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')

        from ..core.texture_atlas import PS1TextureAtlas
        from ..core.mesh_builder import MeshBuilder

        uv_data = uv_layer.data
        for poly in mesh.polygons:
            poly_uvs = [uv_data[i].uv for i in poly.loop_indices]
            is_unmapped = all(abs(u) < 1e-5 and abs(v) < 1e-5 for u, v in poly_uvs)
            if is_unmapped:
                mat_idx = poly.material_index
                rect = None
                if 0 <= mat_idx < len(mesh.materials):
                    mat = mesh.materials[mat_idx]
                    if mat and "atlas_rect" in mat:
                        rect = tuple(mat["atlas_rect"])
                if not rect:
                    rect = MeshBuilder.resolve_uv_rect(mat_idx)

                u0, v0, u1, v1 = rect
                pad_u = min((0.5 / 256.0), (u1 - u0) * 0.04)
                pad_v = min((0.5 / 256.0), (v1 - v0) * 0.04)
                u0_p = u0 + pad_u
                u1_p = u1 - pad_u
                v0_p = v0 + pad_v
                v1_p = v1 - pad_v

                normal = poly.normal
                abs_x, abs_y, abs_z = abs(normal.x), abs(normal.y), abs(normal.z)

                verts = [mesh.vertices[vi] for vi in poly.vertices]
                loop_indices = list(poly.loop_indices)

                if abs_z >= abs_x and abs_z >= abs_y:
                    xs = [v.co.x for v in verts]
                    ys = [v.co.y for v in verts]
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    span_x = max(1e-5, max_x - min_x)
                    span_y = max(1e-5, max_y - min_y)
                    for vi, li in zip(poly.vertices, loop_indices):
                        co = mesh.vertices[vi].co
                        tu = u0_p + ((co.x - min_x) / span_x) * (u1_p - u0_p)
                        tv = v0_p + ((co.y - min_y) / span_y) * (v1_p - v0_p)
                        uv_data[li].uv = (tu, tv)
                elif abs_y >= abs_x:
                    xs = [v.co.x for v in verts]
                    zs = [v.co.z for v in verts]
                    min_x, max_x = min(xs), max(xs)
                    min_z, max_z = min(zs), max(zs)
                    span_x = max(1e-5, max_x - min_x)
                    span_z = max(1e-5, max_z - min_z)
                    for vi, li in zip(poly.vertices, loop_indices):
                        co = mesh.vertices[vi].co
                        tu = u0_p + ((co.x - min_x) / span_x) * (u1_p - u0_p)
                        tv = v0_p + ((co.z - min_z) / span_z) * (v1_p - v0_p)
                        uv_data[li].uv = (tu, tv)
                else:
                    ys = [v.co.y for v in verts]
                    zs = [v.co.z for v in verts]
                    min_y, max_y = min(ys), max(ys)
                    min_z, max_z = min(zs), max(zs)
                    span_y = max(1e-5, max_y - min_y)
                    span_z = max(1e-5, max_z - min_z)
                    for vi, li in zip(poly.vertices, loop_indices):
                        co = mesh.vertices[vi].co
                        tu = u0_p + ((co.y - min_y) / span_y) * (u1_p - u0_p)
                        tv = v0_p + ((co.z - min_z) / span_z) * (v1_p - v0_p)
                        uv_data[li].uv = (tu, tv)

        mesh.update()

    @classmethod
    def export(
        cls,
        obj: bpy.types.Object,
        config: BaseAssetConfig,
        report: ValidationReport,
        filepath: str,
        generator_name: str = "ProceduralAssetGenerator",
        validate_with_godot: bool = True
    ) -> Tuple[str, str, str]:
        """
        Execute full production-grade export pipeline:
        1. Compaction & Material Optimization.
        2. Normal & Shading Normalization (Flat PS1 shading).
        3. Transform Freezing & Pivot Alignment (Bottom Z=0 floor contact).
        4. Godot 4 Collision Mesh & Socket Empties generation.
        5. Clean scene isolation & glTF 2.0 export.
        6. Temporary cleanup.
        7. Metadata Sidecar JSON generation.
        8. Live Godot 4 Headless Verification.
        9. Comprehensive JSON + Markdown Export Reports.

        Returns: (glb_filepath, metadata_json_path, export_report_json_path)
        """
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        warnings_list: List[str] = []

        # 1. Compact materials (purge unreferenced material slots)
        MaterialManager.compact_materials(obj)

        # 1b. Ensure mesh has valid UV map and vertex colors
        cls.ensure_mesh_uvs_and_materials(obj)

        # 2. Normalize normals & shading (PS1 crisp flat shading)
        cls.normalize_mesh_normals(obj)

        # 3. Apply all transforms to visual mesh
        cls.normalize_transforms([obj])

        # 4. Standardize Pivot & Origin (Floor Z=0 contact by default)
        pivot_rule = getattr(config, "pivot_rule", "floor_center")
        min_co, max_co, dims, pivot_delta = cls.normalize_pivot(obj, rule=pivot_rule)
        pivot_info = {
            "rule": pivot_rule,
            "offset": [round(pivot_delta.x, 4), round(pivot_delta.y, 4), round(pivot_delta.z, 4)],
            "bounds_min": [round(min_co.x, 4), round(min_co.y, 4), round(min_co.z, 4)],
            "bounds_max": [round(max_co.x, 4), round(max_co.y, 4), round(max_co.z, 4)],
            "dimensions": [round(dims.x, 4), round(dims.y, 4), round(dims.z, 4)]
        }

        # 5. Build Sockets
        sockets = (config.extra_params.get("sockets") if getattr(config, "extra_params", None) else None) or [
            {
                "name": "socket_player_interact",
                "position": [0.0, -round(dims.y * 0.5 + 0.55, 3), 0.0],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "Standard player character interaction stand point"
            },
            {
                "name": "socket_item_spawn",
                "position": [0.0, 0.0, round(dims.z + 0.02, 3)],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "Prop or pickup spawn snap position (keycards, ammo, medical items)"
            },
            {
                "name": "socket_light",
                "position": [0.0, 0.0, round(dims.z * 0.85, 3)],
                "rotation_deg": [0.0, 0.0, 0.0],
                "description": "OmniLight3D / SpotLight3D mount anchor point"
            }
        ]

        socket_objs = cls.create_socket_nodes(obj, sockets, pivot_delta)

        # 6. Build Godot 4 Collision Shape
        col_obj = cls.create_collision_shape(obj, config, min_co, max_co, dims)
        collision_info = {
            "enabled": col_obj is not None,
            "node_name": col_obj.name if col_obj else "None",
            "shape_type": getattr(config, "collision_type", "box"),
            "godot_suffix": getattr(config, "collision_suffix", "-convcolonly"),
            "extents": [round(dims.x, 4), round(dims.y, 4), round(dims.z, 4)]
        }

        # 7. Isolate export hierarchy (avoid accidental scene leakage)
        export_objects = [obj] + list(obj.children)
        for o in bpy.data.objects:
            o.select_set(False)

        for o in export_objects:
            o.select_set(True)

        bpy.context.view_layer.objects.active = obj

        hierarchy_data = []
        for o in export_objects:
            t_count = len(o.data.polygons) * 2 if (o.type == 'MESH' and o.data) else 0
            v_count = len(o.data.vertices) if (o.type == 'MESH' and o.data) else 0
            hierarchy_data.append({
                "name": o.name,
                "type": o.type,
                "parent": o.parent.name if o.parent else None,
                "triangles": t_count,
                "vertices": v_count
            })

        # Gather materials info
        materials_info = []
        for slot in obj.material_slots:
            if slot.material:
                mat = slot.material
                # Extract metallic and roughness from Principled BSDF
                bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None) if mat.use_nodes else None
                roughness = bsdf.inputs["Roughness"].default_value if bsdf and "Roughness" in bsdf.inputs else 0.5
                metallic = bsdf.inputs["Metallic"].default_value if bsdf and "Metallic" in bsdf.inputs else 0.0
                em_strength = bsdf.inputs["Emission Strength"].default_value if bsdf and "Emission Strength" in bsdf.inputs else 0.0

                materials_info.append({
                    "name": mat.name,
                    "roughness": round(float(roughness), 3),
                    "metallic": round(float(metallic), 3),
                    "emission": f"{round(float(em_strength), 2)}x" if em_strength > 0 else "None"
                })

        try:
            # 8. Export glTF / GLB 2.0 with Godot 4 PBR & vertex colors
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                export_format='GLB',
                use_selection=True,
                export_apply=True,
                export_all_vertex_colors=True,
                export_materials='EXPORT',
                export_image_format='AUTO',
                export_yup=True,
                export_cameras=False,
                export_lights=False,
                export_animations=False
            )
        finally:
            # 9. Clean up temporary collision and socket objects from Blender scene
            if col_obj:
                mesh_to_remove = col_obj.data
                bpy.data.objects.remove(col_obj, do_unlink=True)
                if mesh_to_remove:
                    bpy.data.meshes.remove(mesh_to_remove, do_unlink=True)

            for s_obj in socket_objs:
                bpy.data.objects.remove(s_obj, do_unlink=True)

        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            raise RuntimeError(f"Export failed: GLB file was not created or is empty at {filepath}")

        # 10. Generate Metadata Sidecar JSON
        json_path = save_metadata_sidecar(
            glb_filepath=filepath,
            config=config,
            report=report,
            generator_name=generator_name
        )

        # 11. Run live verification in Godot 4 (if enabled)
        godot_report = None
        if validate_with_godot:
            godot_report = validate_glb_with_godot(filepath)
            if godot_report.get("tested_in_godot") and not godot_report.get("success"):
                warnings_list.append(f"Godot live validation failed: {godot_report.get('errors')}")

        # 12. Generate comprehensive Export Report (JSON and Markdown)
        export_report_json, export_report_md = generate_export_report(
            glb_filepath=filepath,
            config_dict=config.to_dict(),
            validation_dict=report.to_dict(),
            hierarchy_nodes=hierarchy_data,
            materials_list=materials_info,
            collision_info=collision_info,
            sockets_list=sockets,
            godot_validation=godot_report,
            generator_name=generator_name,
            pivot_info=pivot_info,
            warnings=warnings_list
        )

        return ExportResult(filepath, json_path, export_report_json, export_report_md)
