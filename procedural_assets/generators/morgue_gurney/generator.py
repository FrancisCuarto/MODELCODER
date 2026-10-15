import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import MorgueGurneyConfig

class MorgueGurneyGenerator(BaseGenerator):
    """Generates mobile mortuary gurneys with scissor frames, wheels, and optional body bags."""

    def generate(self, config: MorgueGurneyConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        length = config.length
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_wheel = mat_mgr.get_material_index("rubber_tire")
        m_bag = mat_mgr.get_material_index("chair_vinyl")
        m_dark = mat_mgr.get_material_index("casing")
        m_zipper = mat_mgr.get_material_index("switch_metal")

        # 1. Base caster wheels & lower chassis rails
        base_z = 0.08
        wheel_r = 0.06
        wheel_w = 0.04
        x_wheel = (w / 2) - 0.07
        y_wheel = (length / 2) - 0.15

        for wx in (-x_wheel, x_wheel):
            for wy in (-y_wheel, y_wheel):
                # Rubber caster wheel
                MeshBuilder.add_cylinder(bm, (wx, wy, wheel_r), wheel_r, wheel_w, sides=8, axis='X', mat_idx=m_wheel, name="wheel")
                # Swivel fork
                MeshBuilder.add_cylinder(bm, (wx, wy, wheel_r + 0.04), 0.02, 0.06, sides=6, mat_idx=m_steel, name="fork")
                # Brake pedal
                if config.caster_brake_pedals:
                    MeshBuilder.add_box(bm, (wx, wy + 0.05, 0.04), (0.03, 0.05, 0.015), m_dark, "pedal")

        # Lower longitudinal chassis bars
        MeshBuilder.add_box(bm, (-x_wheel, 0, base_z + 0.06), (0.04, length - 0.20, 0.04), m_steel, "lower_rail_L")
        MeshBuilder.add_box(bm, (x_wheel, 0, base_z + 0.06), (0.04, length - 0.20, 0.04), m_steel, "lower_rail_R")
        # Lower crossbars
        MeshBuilder.add_box(bm, (0, -y_wheel, base_z + 0.06), (w - 0.14, 0.04, 0.04), m_steel, "lower_cross_1")
        MeshBuilder.add_box(bm, (0, y_wheel, base_z + 0.06), (w - 0.14, 0.04, 0.04), m_steel, "lower_cross_2")

        # 2. Scissor elevation frame (X-braces on each side)
        tray_z = h - 0.08
        if config.has_scissor_lift:
            scissor_z_mid = (base_z + tray_z) / 2
            z_span = tray_z - base_z
            y_span = length * 0.55
            tube_r = 0.022

            for sx in (-x_wheel + 0.01, x_wheel - 0.01):
                # Diagonal strut 1
                p1_start = Vector((sx, -y_span / 2, base_z + 0.08))
                p1_end = Vector((sx, y_span / 2, tray_z - 0.02))
                MeshBuilder.add_extruded_cable(bm, [p1_start, p1_end], radius=tube_r, sides=4, mat_idx=m_steel, name="scissor_strut_1")

                # Diagonal strut 2 (crossing)
                p2_start = Vector((sx, y_span / 2, base_z + 0.08))
                p2_end = Vector((sx, -y_span / 2, tray_z - 0.02))
                MeshBuilder.add_extruded_cable(bm, [p2_start, p2_end], radius=tube_r, sides=4, mat_idx=m_steel, name="scissor_strut_2")

                # Central pivot pin
                MeshBuilder.add_cylinder(bm, (sx, 0, scissor_z_mid), 0.035, 0.03, sides=6, axis='X', mat_idx=m_dark, name="pivot_pin")
        else:
            # 4 Vertical straight struts
            for sx in (-x_wheel, x_wheel):
                for sy in (-y_wheel * 0.7, y_wheel * 0.7):
                    MeshBuilder.add_cylinder(bm, (sx, sy, (base_z + tray_z) / 2), 0.025, tray_z - base_z, sides=6, mat_idx=m_steel, name="upright")

        # 3. Upper Tray Support Frame & Push Handles
        MeshBuilder.add_box(bm, (0, 0, tray_z), (w - 0.06, length - 0.10, 0.04), m_steel, "upper_frame")

        if config.has_push_handles:
            # Tubular push handle loops on head & foot ends
            for hy in (-(length / 2) + 0.02, (length / 2) - 0.02):
                h_dir = -1 if hy < 0 else 1
                # Upright posts
                MeshBuilder.add_cylinder(bm, (-w / 3, hy + (h_dir * 0.04), tray_z + 0.12), 0.018, 0.24, sides=4, mat_idx=m_steel, name="handle_post_L")
                MeshBuilder.add_cylinder(bm, (w / 3, hy + (h_dir * 0.04), tray_z + 0.12), 0.018, 0.24, sides=4, mat_idx=m_steel, name="handle_post_R")
                # Top horizontal grip
                MeshBuilder.add_cylinder(bm, (0, hy + (h_dir * 0.04), tray_z + 0.24), 0.018, w * 0.66, sides=4, axis='X', mat_idx=m_steel, name="handle_grip")

        # 4. Stainless Steel Body Tray
        tray_top_z = tray_z + 0.04
        tray_th = 0.03
        MeshBuilder.add_box(bm, (0, 0, tray_top_z), (w, length, tray_th), m_steel, "body_tray_slab")
        # Perimeter tray raised lip
        lip_h = 0.04
        lip_t = 0.025
        MeshBuilder.add_box(bm, (-(w / 2 - lip_t / 2), 0, tray_top_z + lip_h / 2), (lip_t, length, lip_h), m_steel, "tray_rim_L")
        MeshBuilder.add_box(bm, ((w / 2 - lip_t / 2), 0, tray_top_z + lip_h / 2), (lip_t, length, lip_h), m_steel, "tray_rim_R")
        MeshBuilder.add_box(bm, (0, -(length / 2 - lip_t / 2), tray_top_z + lip_h / 2), (w - lip_t * 2, lip_t, lip_h), m_steel, "tray_rim_bot")
        MeshBuilder.add_box(bm, (0, (length / 2 - lip_t / 2), tray_top_z + lip_h / 2), (w - lip_t * 2, lip_t, lip_h), m_steel, "tray_rim_top")

        # 5. Body Bag Silhouette
        if config.gurney_type in ("body_bag_closed", "body_bag_ajar"):
            bag_h = config.body_silhouette_height
            bag_w = w * 0.65
            bag_l = length * 0.85
            bag_z = tray_top_z + tray_th / 2 + bag_h / 2

            # Main torso/body volume (tapered low-poly body bag)
            MeshBuilder.add_box(bm, (0, -0.05, bag_z), (bag_w, bag_l, bag_h), m_bag, "body_bag_main")

            # Raised chest / torso prominence
            MeshBuilder.add_box(bm, (0, 0.15, bag_z + bag_h * 0.20), (bag_w * 0.85, bag_l * 0.35, bag_h * 0.40), m_bag, "bag_chest")

            # Feet protrusion
            MeshBuilder.add_box(bm, (0, -0.70, bag_z - bag_h * 0.15), (bag_w * 0.60, 0.25, bag_h * 0.50), m_bag, "bag_feet")

            # Longitudinal zipper seam
            zipper_z = bag_z + bag_h / 2 + 0.005
            MeshBuilder.add_box(bm, (0, -0.05, zipper_z), (0.02, bag_l * 0.90, 0.01), m_zipper, "zipper_track")

            if config.gurney_type == "body_bag_ajar":
                # Peeled open flap exposing dark interior at the head
                flap_x = bag_w * 0.22
                flap_y = (bag_l / 2) - 0.20
                MeshBuilder.add_box(bm, (flap_x, flap_y, zipper_z + 0.03), (0.12, 0.28, 0.02), m_dark, "open_flap_reveal")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
