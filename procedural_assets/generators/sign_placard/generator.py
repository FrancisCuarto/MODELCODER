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
from .config import SignPlacardConfig

class SignPlacardGenerator(BaseAssetGenerator[SignPlacardConfig]):
    """
    Procedural generator for facility signage, danger placards, and evacuation markers.
    """

    def generate(self, config: SignPlacardConfig) -> bpy.types.Object:
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

        # Material & Rect selection based on sign type
        if config.sign_type == "emergency_exit":
            face_rect = PS1TextureAtlas.get_rect("sign_exit_green")
            face_mat = m_idx.get("sign_exit", 0)
            face_rgba = rgba.get("sign_exit", (0.08, 0.65, 0.25, 1.0))
        elif config.sign_type == "sector_id":
            face_rect = PS1TextureAtlas.get_rect("sign_sector_blue")
            face_mat = m_idx.get("sign_sector", 0)
            face_rgba = rgba.get("sign_sector", (0.1, 0.3, 0.6, 1.0))
        elif config.sign_type == "high_voltage":
            face_rect = PS1TextureAtlas.get_rect("door_seal_red")
            face_mat = m_idx.get("door_emergency_red", 0)
            face_rgba = rgba.get("door_emergency_red", (0.7, 0.1, 0.1, 1.0))
        else:
            # "hazard_biohazard"
            face_rect = PS1TextureAtlas.get_rect("caution_label")
            face_mat = m_idx.get("sign_caution", m_idx.get("hazard_yellow", 0))
            face_rgba = rgba.get("sign_caution", (0.85, 0.65, 0.05, 1.0))

        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")

        w = config.width
        h = config.height
        d = config.depth

        tilt_angle = 0.0
        if config.damage_style == "hanging_crooked" and config.mount_type == "ceiling_hanging":
            tilt_angle = math.radians(14.0)

        rot_mat = mathutils.Matrix.Rotation(tilt_angle, 4, 'Z')

        # -------------------------------------------------------------------------
        # 1. Backing Enclosure Box / Frame
        # -------------------------------------------------------------------------
        frame_margin = 0.02
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((w, h, d)),
            offset=mathutils.Vector((0.0, 0.0, -d / 2.0)),
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.15, 0.16, 0.18, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_dark_rect
        )

        # -------------------------------------------------------------------------
        # 2. Front Placard Face Plate
        # -------------------------------------------------------------------------
        face_faces = MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((w - frame_margin * 2, h - frame_margin * 2, 0.008)),
            offset=mathutils.Vector((0.0, 0.0, 0.004)),
            mat_idx=face_mat,
            rgba=face_rgba,
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=face_rect
        )

        # Bent corner damage (bottom-right corner curled out)
        if config.damage_style == "bent_corner":
            for f in face_faces:
                for v in f.verts:
                    if v.co.x > (w * 0.35) and v.co.y < -(h * 0.30):
                        v.co.z += 0.045
                        v.co.x -= 0.015

        # -------------------------------------------------------------------------
        # 3. Corner Fasteners
        # -------------------------------------------------------------------------
        if config.has_corner_bolts and config.mount_type == "wall_flush":
            bx = (w / 2.0) - 0.025
            by = (h / 2.0) - 0.025
            for sx in (-bx, bx):
                for sy in (-by, by):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.008,
                        depth=0.012,
                        segments=4,
                        offset=mathutils.Vector((sx, sy, 0.006)),
                        axis='Z',
                        mat_idx=m_idx.get("screw", 0),
                        rgba=rgba.get("screw", (0.7, 0.7, 0.7, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect,
                        smooth=False
                    )

        # -------------------------------------------------------------------------
        # 4. Mounting Hardware
        # -------------------------------------------------------------------------
        if config.mount_type == "ceiling_hanging":
            chain_len = config.hanging_chain_length
            chain_spacing = w * 0.70

            for ci, side in enumerate((-1.0, 1.0)):
                # If crooked damage, one chain has snapped and hangs empty or is missing!
                if config.damage_style == "hanging_crooked" and side == 1.0:
                    # Snapped short stub of chain
                    hang_pts = [
                        mathutils.Vector((side * (chain_spacing / 2.0), (h / 2.0), -d / 2.0)),
                        mathutils.Vector((side * (chain_spacing / 2.0), (h / 2.0) + 0.08, -d / 2.0))
                    ]
                else:
                    hang_pts = [
                        mathutils.Vector((side * (chain_spacing / 2.0), (h / 2.0), -d / 2.0)),
                        mathutils.Vector((side * (chain_spacing / 2.0), (h / 2.0) + chain_len, -d / 2.0))
                    ]

                MeshBuilder.add_extruded_cable(
                    bm=bm,
                    points=hang_pts,
                    radius=0.008,
                    sides=4,
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.5, 0.5, 0.5, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

        elif config.mount_type == "flag_perpendicular":
            # Wall mounting bracket extending from left edge
            bracket_x = -(w / 2.0) - 0.04
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.08, h * 0.9, 0.02)),
                offset=mathutils.Vector((bracket_x, 0.0, -d / 2.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.2, 0.22, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

        # Apply crooked rotation to entire mesh if requested
        if tilt_angle != 0.0:
            bm.verts.ensure_lookup_table()
            for v in bm.verts:
                v.co = rot_mat @ v.co

        bmesh.ops.rotate(
            bm,
            cent=(0.0, 0.0, 0.0),
            matrix=mathutils.Matrix.Rotation(math.radians(90.0), 3, 'X'),
            verts=bm.verts
        )
        min_z = min(v.co.z for v in bm.verts)
        bmesh.ops.translate(
            bm,
            vec=(0.0, 0.0, -min_z),
            verts=bm.verts
        )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

