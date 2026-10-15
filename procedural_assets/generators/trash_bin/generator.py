import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import TrashBinConfig

class TrashBinGenerator(BaseAssetGenerator[TrashBinConfig]):
    """
    Procedural generator for industrial trash cans, pedal bins, and biohazard drums.
    """

    def generate(self, config: TrashBinConfig) -> bpy.types.Object:
        self.clean_context()
        rng = random.Random(config.seed)

        self.material_manager = self.get_material_manager(config)
        mesh_name = f"{config.name}_mesh"
        obj_name = config.name

        if obj_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)
        if mesh_name in bpy.data.meshes:
            bpy.data.meshes.remove(bpy.data.meshes[mesh_name], do_unlink=True)

        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)

        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices
        rgba = {k: self.material_manager.get_rgba(k) for k in self.material_manager.palette.keys()}

        bm = bmesh.new()
        col_layer = bm.loops.layers.color.new("Color")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        # Atlas textures
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        hazard_rect = PS1TextureAtlas.get_rect("hazard_stripes")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")

        h = config.height
        rad = config.radius
        w = config.width
        d = config.depth

        body_mat = m_idx.get("casing", 0)
        body_rgba = rgba.get("casing", (0.22, 0.24, 0.26, 1.0))

        if config.bin_type == "drum_hazard":
            body_mat = m_idx.get("hazard_yellow", 0)
            body_rgba = rgba.get("hazard_yellow", (0.85, 0.65, 0.1, 1.0))
            body_rect = hazard_rect
        else:
            body_rect = metal_dark_rect

        # -------------------------------------------------------------------------
        # 1. Main Bin Body (Cylinder or Box)
        # -------------------------------------------------------------------------
        if config.is_rectangular or config.bin_type == "office_basket":
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w, h, d)),
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                mat_idx=body_mat,
                rgba=body_rgba,
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=body_rect
            )
            # Top perimeter lip
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 1.05, 0.02, d * 1.05)),
                offset=mathutils.Vector((0.0, h, 0.0)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect
            )
        else:
            # Cylindrical container
            segments = 8 if config.target_tri_budget > 300 else 6
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad,
                depth=h,
                segments=segments,
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                axis='Y',
                mat_idx=body_mat,
                rgba=body_rgba,
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=body_rect,
                smooth=False
            )
            # Top retaining rim
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad * 1.05,
                depth=0.025,
                segments=segments,
                offset=mathutils.Vector((0.0, h - 0.0125, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.5, 0.5, 0.5, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect,
                smooth=False
            )

        # -------------------------------------------------------------------------
        # 2. Foot Pedal & Mechanical Linkage (Step Can)
        # -------------------------------------------------------------------------
        if config.has_foot_pedal and config.bin_type == "pedal_can":
            pedal_w = 0.08
            pedal_d = 0.06
            pedal_z = (d / 2.0 if config.is_rectangular else rad) + (pedal_d / 2.0)
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((pedal_w, 0.015, pedal_d)),
                offset=mathutils.Vector((0.0, 0.025, pedal_z)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect
            )
            # Rubber grip pad on pedal
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((pedal_w * 0.8, 0.008, pedal_d * 0.7)),
                offset=mathutils.Vector((0.0, 0.035, pedal_z)),
                mat_idx=m_idx.get("switch_base", 0),
                rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=rubber_rect
            )

        # -------------------------------------------------------------------------
        # 3. Hinged Lid with Angle Variation
        # -------------------------------------------------------------------------
        if config.lid_state != "missing" and config.bin_type != "office_basket":
            if config.lid_state == "closed":
                lid_ang = 0.0
            elif config.lid_state == "open_wide":
                lid_ang = math.radians(80.0)
            else:
                # "ajar"
                lid_ang = math.radians(config.lid_open_angle)

            lid_t = 0.02
            hinge_z = -(d / 2.0 if config.is_rectangular else rad)
            hinge_y = h

            # Build lid at origin, rotate around X-axis, translate to hinge
            lid_rad = rad * 1.06
            lid_geom = bmesh.ops.create_cone(
                bm,
                cap_ends=True,
                cap_tris=False,
                segments=8,
                radius1=lid_rad,
                radius2=lid_rad,
                depth=lid_t
            )
            lid_verts = [v for v in lid_geom["verts"] if isinstance(v, bmesh.types.BMVert)]

            rot_x = mathutils.Matrix.Rotation(-lid_ang, 4, 'X')
            for v in lid_verts:
                # Rotate around hinge position (z = -lid_rad)
                v.co.z += lid_rad  # Move center forward relative to hinge
                v.co = rot_x @ v.co
                v.co.z += hinge_z
                v.co.y += hinge_y

            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                if all(v in lid_verts for v in f.verts):
                    MeshBuilder.apply_face_attributes(f, body_mat, body_rgba, col_layer, smooth=False)
                    if uv_layer:
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, metal_light_rect)

        # -------------------------------------------------------------------------
        # 4. Overflowing Trash & Biohazard Bags
        # -------------------------------------------------------------------------
        if config.has_overflowing_trash:
            # Crumpled mass poking out the top
            trash_faces = MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((rad * 1.1, 0.09, rad * 1.1)),
                offset=mathutils.Vector((0.0, h + 0.02, 0.0)),
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.2, 0.25, 0.18, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )
            # Add jitter to trash verts for crumpled look
            for f in trash_faces:
                for v in f.verts:
                    v.co.x += rng.uniform(-0.025, 0.025)
                    v.co.z += rng.uniform(-0.025, 0.025)

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
