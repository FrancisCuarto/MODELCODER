import math
import mathutils
import bmesh
import bpy

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import NightstandConfig

class NightstandGenerator(BaseAssetGenerator):
    """Procedural generator for crew nightstands, bedside lockers, and medical side carts."""

    def generate(self, config: NightstandConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        w = config.width
        d = config.depth
        h = config.height
        half_w = w * 0.5
        half_d = d * 0.5

        # Materials
        m_casing = mat_mgr.get_index("wall_bulkhead")
        r_casing = mat_mgr.get_rect("metal_dark_grime")

        m_trim = mat_mgr.get_index("wall_support_beam")
        r_trim = mat_mgr.get_rect("metal_light_brushed")

        m_drawer = mat_mgr.get_index("locker_gray")
        r_drawer = mat_mgr.get_rect("beige_plastic_worn")

        m_rubber = mat_mgr.get_index("rubber_tire")
        r_rubber = mat_mgr.get_rect("rubber_black")

        m_lamp = mat_mgr.get_index("fluorescent_tube_lit")
        r_lamp = mat_mgr.get_rect("fluorescent_lit")
        if config.lamp_state == "flickering":
            m_lamp = mat_mgr.get_index("led_yellow")
            r_lamp = mat_mgr.get_rect("led_yellow")
        elif config.lamp_state == "off":
            m_lamp = mat_mgr.get_index("glass_tube")
            r_lamp = mat_mgr.get_rect("crt_screen_off")

        # -------------------------------------------------------------
        # 1. BASE & LEGS
        # -------------------------------------------------------------
        leg_h = 0.08
        if config.stand_type == "medical_tray_cart":
            leg_h = 0.10
            # 4 Caster Wheels
            wheel_rad = 0.04
            for cx in [-half_w + 0.05, half_w - 0.05]:
                for cy in [-half_d + 0.05, half_d - 0.05]:
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=wheel_rad,
                        depth=0.03,
                        segments=6,
                        offset=mathutils.Vector((cx, cy, wheel_rad)),
                        axis='X',
                        mat_idx=m_rubber,
                        uv_layer=uv_layer,
                        uv_rect=r_rubber,
                        color_layer=color_layer
                    )
        elif config.stand_type == "wall_mounted":
            leg_h = 0.0
            # Diagonal wall mounting brackets on the back (+Y)
            bracket_thick = 0.04
            for bx in [-half_w + 0.06, half_w - 0.06]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((bracket_thick, 0.12, 0.20)),
                    offset=mathutils.Vector((bx, half_d - 0.04, 0.10)),
                    mat_idx=m_trim,
                    uv_layer=uv_layer,
                    uv_rect=r_trim,
                    color_layer=color_layer
                )
        else:
            # 4 Plinth Foot Pegs
            peg_thick = 0.045
            for px in [-half_w + 0.03, half_w - 0.03]:
                for py in [-half_d + 0.03, half_d - 0.03]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((peg_thick, peg_thick, leg_h)),
                        offset=mathutils.Vector((px, py, leg_h * 0.5)),
                        mat_idx=m_rubber,
                        uv_layer=uv_layer,
                        uv_rect=r_rubber,
                        color_layer=color_layer
                    )

        # -------------------------------------------------------------
        # 2. MAIN CABINET BODY
        # -------------------------------------------------------------
        body_h = h - leg_h
        body_z = leg_h + body_h * 0.5
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, d, body_h)),
            offset=mathutils.Vector((0.0, 0.0, body_z)),
            mat_idx=m_casing,
            uv_layer=uv_layer,
            uv_rect=r_casing,
            color_layer=color_layer,
            rgba=(0.26, 0.28, 0.30, 1.0)
        )

        # Raised Tabletop Retaining Lip (Anti-slide)
        if config.has_raised_rim:
            lip_h = 0.03
            lip_thick = 0.02
            # Left lip
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((lip_thick, d, lip_h)),
                offset=mathutils.Vector((-half_w + lip_thick * 0.5, 0.0, h + lip_h * 0.5)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Right lip
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((lip_thick, d, lip_h)),
                offset=mathutils.Vector((half_w - lip_thick * 0.5, 0.0, h + lip_h * 0.5)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Back lip
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, lip_thick, lip_h)),
                offset=mathutils.Vector((0.0, half_d - lip_thick * 0.5, h + lip_h * 0.5)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )

        # -------------------------------------------------------------
        # 3. DRAWERS / OPEN CUBBY
        # -------------------------------------------------------------
        drawer_gap = 0.02
        front_y = -half_d - 0.015

        if config.stand_type == "crew_locker_cubby":
            # 1 Top Drawer + 1 Lower Open Cubby
            drw_h = body_h * 0.38
            cubby_h = body_h * 0.48
            drw_z = leg_h + body_h - drw_h * 0.5 - 0.03
            # Top drawer pullout offset
            pull_y = front_y - (d * 0.35 * config.drawer_open_ratio)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.88, 0.03, drw_h)),
                offset=mathutils.Vector((0.0, pull_y, drw_z)),
                mat_idx=m_drawer,
                uv_layer=uv_layer,
                uv_rect=r_drawer,
                color_layer=color_layer,
                rgba=(0.35, 0.37, 0.40, 1.0)
            )
            # Handle lip
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.14, 0.02, 0.03)),
                offset=mathutils.Vector((0.0, pull_y - 0.015, drw_z + drw_h * 0.25)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Recessed cubby cavity
            cubby_z = leg_h + cubby_h * 0.5 + 0.03
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.84, 0.03, cubby_h)),
                offset=mathutils.Vector((0.0, front_y + 0.04, cubby_z)),
                mat_idx=m_casing,
                uv_layer=uv_layer,
                uv_rect=r_casing,
                color_layer=color_layer,
                rgba=(0.14, 0.15, 0.16, 1.0)
            )

        else: # sliding_drawers / medical_tray_cart
            count = max(1, min(3, config.drawer_count))
            each_h = (body_h - (drawer_gap * (count + 1))) / count
            for i in range(count):
                cur_z = leg_h + drawer_gap + (each_h * 0.5) + (i * (each_h + drawer_gap))
                # Top drawer slides out if drawer_open_ratio > 0
                is_top = (i == count - 1)
                pull_y = front_y - (d * 0.35 * config.drawer_open_ratio if is_top else 0.0)
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((w * 0.88, 0.03, each_h)),
                    offset=mathutils.Vector((0.0, pull_y, cur_z)),
                    mat_idx=m_drawer,
                    uv_layer=uv_layer,
                    uv_rect=r_drawer,
                    color_layer=color_layer,
                    rgba=(0.35, 0.37, 0.40, 1.0)
                )
                # Pull handle
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.14, 0.02, 0.03)),
                    offset=mathutils.Vector((0.0, pull_y - 0.015, cur_z)),
                    mat_idx=m_trim,
                    uv_layer=uv_layer,
                    uv_rect=r_trim,
                    color_layer=color_layer
                )

        # -------------------------------------------------------------
        # 4. BEDSIDE LAMP
        # -------------------------------------------------------------
        if config.has_bedside_lamp:
            lamp_x = half_w - 0.08
            lamp_y = half_d - 0.08
            # Base clamp / foot
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.07, 0.07, 0.02)),
                offset=mathutils.Vector((lamp_x, lamp_y, h + 0.01)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Gooseneck stem
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.018, 0.018, 0.16)),
                offset=mathutils.Vector((lamp_x, lamp_y, h + 0.09)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Angled head arm
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.018, 0.08, 0.018)),
                offset=mathutils.Vector((lamp_x, lamp_y - 0.03, h + 0.17)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Lamp shade / cowl
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.06, 0.08, 0.05)),
                offset=mathutils.Vector((lamp_x, lamp_y - 0.07, h + 0.17)),
                mat_idx=m_casing,
                uv_layer=uv_layer,
                uv_rect=r_casing,
                color_layer=color_layer
            )
            # Emissive bulb face
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.045, 0.06, 0.01)),
                offset=mathutils.Vector((lamp_x, lamp_y - 0.07, h + 0.145)),
                mat_idx=m_lamp,
                uv_layer=uv_layer,
                uv_rect=r_lamp,
                color_layer=color_layer,
                rgba=(0.95, 0.95, 0.85, 1.0)
            )

        # -------------------------------------------------------------
        # 5. OVER-BED SWIVEL TRAY ARM
        # -------------------------------------------------------------
        if config.has_swivel_tray or config.stand_type == "medical_tray_cart":
            mast_x = -half_w - 0.03
            mast_y = half_d - 0.06
            mast_h = 0.35
            # Vertical mast
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.035, 0.035, mast_h)),
                offset=mathutils.Vector((mast_x, mast_y, h + mast_h * 0.5)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )
            # Articulated swing arm
            tray_len = 0.40
            tray_w = 0.28
            tray_z = h + mast_h
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((tray_w, tray_len, 0.025)),
                offset=mathutils.Vector((mast_x - tray_w * 0.4, 0.0, tray_z)),
                mat_idx=m_trim,
                uv_layer=uv_layer,
                uv_rect=r_trim,
                color_layer=color_layer
            )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: NightstandConfig) -> ValidationReport:
        return super().validate(obj, config)
