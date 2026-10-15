import math
import mathutils
import bmesh
import bpy

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import OfficeDoorConfig

class OfficeDoorGenerator(BaseAssetGenerator):
    """Procedural generator for glazed office, clinic, and laboratory doors."""

    def generate(self, config: OfficeDoorConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        w = config.width
        h = config.height
        fd = config.frame_depth
        half_w = w * 0.5

        # Materials
        m_frame = mat_mgr.get_index("door_frame_heavy")
        r_frame = mat_mgr.get_rect("metal_dark_grime")

        m_leaf = mat_mgr.get_index("locker_gray")
        r_leaf = mat_mgr.get_rect("beige_plastic_worn")

        m_glass = mat_mgr.get_index("glass_observation")
        r_glass = mat_mgr.get_rect("glass_observation")

        m_trim = mat_mgr.get_index("wall_support_beam")
        r_trim = mat_mgr.get_rect("metal_light_brushed")

        m_kick = mat_mgr.get_index("mounting")
        r_kick = mat_mgr.get_rect("metal_light_brushed")

        m_rust = mat_mgr.get_index("rust_patch")
        r_rust = mat_mgr.get_rect("rust_heavy")

        # -------------------------------------------------------------
        # 1. OUTER DOOR FRAME (Jambs, Header, Threshold)
        # -------------------------------------------------------------
        jamb_thick = 0.08
        header_h = 0.10
        inner_w = w - (jamb_thick * 2.0)
        inner_h = h - header_h

        # Transom window split if enabled
        transom_h = 0.45 if config.has_transom else 0.0
        door_clear_h = inner_h - transom_h

        # Left Jamb (-X)
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((jamb_thick, fd, h)),
            offset=mathutils.Vector((-half_w + jamb_thick * 0.5, 0.0, h * 0.5)),
            mat_idx=m_frame,
            uv_layer=uv_layer,
            uv_rect=r_frame,
            color_layer=color_layer,
            rgba=(0.20, 0.22, 0.24, 1.0)
        )
        # Right Jamb (+X)
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((jamb_thick, fd, h)),
            offset=mathutils.Vector((half_w - jamb_thick * 0.5, 0.0, h * 0.5)),
            mat_idx=m_frame,
            uv_layer=uv_layer,
            uv_rect=r_frame,
            color_layer=color_layer,
            rgba=(0.20, 0.22, 0.24, 1.0)
        )
        # Top Header Lintel
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, fd, header_h)),
            offset=mathutils.Vector((0.0, 0.0, h - header_h * 0.5)),
            mat_idx=m_frame,
            uv_layer=uv_layer,
            uv_rect=r_frame,
            color_layer=color_layer,
            rgba=(0.20, 0.22, 0.24, 1.0)
        )

        # Transom Window
        if config.has_transom:
            transom_mullion_h = 0.06
            transom_z = door_clear_h + transom_mullion_h * 0.5
            # Intermediate mullion bar
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((inner_w, fd * 0.85, transom_mullion_h)),
                offset=mathutils.Vector((0.0, 0.0, transom_z)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            # Transom glass
            transom_glass_h = transom_h - transom_mullion_h
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((inner_w * 0.95, 0.03, transom_glass_h * 0.90)),
                offset=mathutils.Vector((0.0, 0.0, door_clear_h + transom_mullion_h + transom_glass_h * 0.5)),
                mat_idx=m_glass,
                uv_layer=uv_layer,
                uv_rect=r_glass,
                color_layer=color_layer,
                rgba=(0.08, 0.12, 0.16, 0.85)
            )

        # -------------------------------------------------------------
        # 2. DOOR LEAF / PANELS (With pivot open angle)
        # -------------------------------------------------------------
        leaf_thick = 0.045
        open_rad = math.radians(min(95.0, max(0.0, config.open_angle_deg)))

        def build_single_leaf(leaf_w: float, pivot_x: float, sign_dir: float):
            """Builds a door leaf rotated around pivot_x by open_rad."""
            leaf_h = door_clear_h - 0.02

            # Rotation matrix around pivot point (pivot_x, 0, 0)
            rot_mat = mathutils.Matrix.Rotation(sign_dir * open_rad, 4, 'Z')
            piv_vec = mathutils.Vector((pivot_x, 0.0, 0.0))

            def transform_pt(local_pt: mathutils.Vector) -> mathutils.Vector:
                return piv_vec + rot_mat @ (local_pt - piv_vec)

            # Local center of leaf when closed
            center_x = pivot_x + (sign_dir * leaf_w * 0.5)

            # Glazed window cutout dimensions
            win_w = leaf_w * 0.55
            win_h = leaf_h * 0.45
            win_z = leaf_h * 0.62  # Centered at eye level
            win_x = center_x

            # Frame around leaf window:
            # 1. Bottom section (with kickplate)
            bot_h = win_z - (win_h * 0.5)
            geom_bot = bmesh.ops.create_cube(bm, size=1.0)
            v_bot = [v for v in geom_bot["verts"] if isinstance(v, bmesh.types.BMVert)]
            for v in v_bot:
                v.co.x = v.co.x * leaf_w + center_x
                v.co.y = v.co.y * leaf_thick
                v.co.z = v.co.z * bot_h + (bot_h * 0.5)
                v.co = transform_pt(v.co)
            for f in bm.faces:
                if all(vt in set(v_bot) for vt in f.verts):
                    MeshBuilder.apply_face_attributes(f, m_leaf, (0.35, 0.38, 0.40, 1.0), color_layer)
                    MeshBuilder.apply_face_uv_rect(f, uv_layer, r_leaf)

            # Kickplate on bottom 0.22m
            if config.has_kickplate:
                kp_h = 0.22
                geom_kp = bmesh.ops.create_cube(bm, size=1.0)
                v_kp = [v for v in geom_kp["verts"] if isinstance(v, bmesh.types.BMVert)]
                for v in v_kp:
                    v.co.x = v.co.x * (leaf_w - 0.02) + center_x
                    v.co.y = v.co.y * (leaf_thick + 0.01)
                    v.co.z = v.co.z * kp_h + (kp_h * 0.5)
                    v.co = transform_pt(v.co)
                for f in bm.faces:
                    if all(vt in set(v_kp) for vt in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_kick, (0.6, 0.6, 0.6, 1.0), color_layer)
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, r_kick)

            # 2. Top section above window
            top_h = leaf_h - (win_z + win_h * 0.5)
            geom_top = bmesh.ops.create_cube(bm, size=1.0)
            v_top = [v for v in geom_top["verts"] if isinstance(v, bmesh.types.BMVert)]
            for v in v_top:
                v.co.x = v.co.x * leaf_w + center_x
                v.co.y = v.co.y * leaf_thick
                v.co.z = v.co.z * top_h + (leaf_h - top_h * 0.5)
                v.co = transform_pt(v.co)
            for f in bm.faces:
                if all(vt in set(v_top) for vt in f.verts):
                    MeshBuilder.apply_face_attributes(f, m_leaf, (0.35, 0.38, 0.40, 1.0), color_layer)
                    MeshBuilder.apply_face_uv_rect(f, uv_layer, r_leaf)

            # 3. Left and right window stiles
            stile_w = (leaf_w - win_w) * 0.5
            for sign_s, st_x in [(-1, center_x - leaf_w * 0.5 + stile_w * 0.5), (1, center_x + leaf_w * 0.5 - stile_w * 0.5)]:
                geom_st = bmesh.ops.create_cube(bm, size=1.0)
                v_st = [v for v in geom_st["verts"] if isinstance(v, bmesh.types.BMVert)]
                for v in v_st:
                    v.co.x = v.co.x * stile_w + st_x
                    v.co.y = v.co.y * leaf_thick
                    v.co.z = v.co.z * win_h + win_z
                    v.co = transform_pt(v.co)
                for f in bm.faces:
                    if all(vt in set(v_st) for vt in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_leaf, (0.35, 0.38, 0.40, 1.0), color_layer)
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, r_leaf)

            # 4. Glazed window pane
            if config.glass_damage != "shattered_missing":
                geom_gl = bmesh.ops.create_cube(bm, size=1.0)
                v_gl = [v for v in geom_gl["verts"] if isinstance(v, bmesh.types.BMVert)]
                for v in v_gl:
                    v.co.x = v.co.x * (win_w - 0.02) + win_x
                    v.co.y = v.co.y * 0.015
                    v.co.z = v.co.z * (win_h - 0.02) + win_z
                    v.co = transform_pt(v.co)
                for f in bm.faces:
                    if all(vt in set(v_gl) for vt in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_glass, (0.10, 0.14, 0.18, 0.85), color_layer)
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, r_glass)

            # 5. Handle / Push Bar
            bar_y = -leaf_thick * 0.5 - 0.025
            bar_z = leaf_h * 0.48
            if config.handle_type == "horizontal_push_bar":
                geom_pb = bmesh.ops.create_cube(bm, size=1.0)
                v_pb = [v for v in geom_pb["verts"] if isinstance(v, bmesh.types.BMVert)]
                for v in v_pb:
                    v.co.x = v.co.x * (leaf_w * 0.75) + center_x
                    v.co.y = v.co.y * 0.035 + bar_y
                    v.co.z = v.co.z * 0.045 + bar_z
                    v.co = transform_pt(v.co)
                for f in bm.faces:
                    if all(vt in set(v_pb) for vt in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_trim, (0.7, 0.7, 0.7, 1.0), color_layer)
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, r_trim)

            elif config.handle_type == "industrial_lever":
                h_x = center_x + (sign_dir * (leaf_w * 0.35))
                geom_lv = bmesh.ops.create_cube(bm, size=1.0)
                v_lv = [v for v in geom_lv["verts"] if isinstance(v, bmesh.types.BMVert)]
                for v in v_lv:
                    v.co.x = v.co.x * 0.12 + h_x
                    v.co.y = v.co.y * 0.04 + bar_y
                    v.co.z = v.co.z * 0.025 + bar_z
                    v.co = transform_pt(v.co)
                for f in bm.faces:
                    if all(vt in set(v_lv) for vt in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_trim, (0.7, 0.7, 0.7, 1.0), color_layer)
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, r_trim)

        if config.door_style == "double_swing":
            half_leaf_w = inner_w * 0.5
            # Left Leaf (pivots at left jamb)
            build_single_leaf(leaf_w=half_leaf_w, pivot_x=-half_w + jamb_thick, sign_dir=1.0)
            # Right Leaf (pivots at right jamb)
            build_single_leaf(leaf_w=half_leaf_w, pivot_x=half_w - jamb_thick, sign_dir=-1.0)
        else: # single_swing / sliding_pocket
            build_single_leaf(leaf_w=inner_w, pivot_x=-half_w + jamb_thick, sign_dir=1.0)

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: OfficeDoorConfig) -> ValidationReport:
        return super().validate(obj, config)
