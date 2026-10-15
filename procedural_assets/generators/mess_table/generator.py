import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import MessTableConfig

class MessTableGenerator(BaseGenerator):
    """Generates space station mess hall tables with attached swivel stools and food trays."""

    def generate(self, config: MessTableConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.table_width
        length = config.table_length
        h = config.table_height

        m_steel = mat_mgr.get_material_index("mounting")
        m_top = mat_mgr.get_material_index("locker_gray")
        m_frame = mat_mgr.get_material_index("casing")
        m_stool = mat_mgr.get_material_index("chair_vinyl")
        m_tray = mat_mgr.get_material_index("metal_dark_grime") if "metal_dark_grime" in mat_mgr.palette else m_steel

        # 1. Central Support Pedestals & Floor Flanges
        ped_r = 0.05
        ped_y_offset = length * 0.28
        for py in (-ped_y_offset, ped_y_offset):
            # Vertical column
            MeshBuilder.add_cylinder(bm, (0, py, h / 2), ped_r, h - 0.05, sides=6, mat_idx=m_frame, name="pedestal_col")
            # Floor flange
            if config.has_floor_bolts:
                MeshBuilder.add_cylinder(bm, (0, py, 0.02), ped_r + 0.05, 0.04, sides=6, mat_idx=m_steel, name="floor_flange")
                MeshBuilder.add_cylinder(bm, (0, py + 0.06, 0.04), 0.012, 0.02, sides=4, mat_idx=m_steel, name="bolt")

        # Longitudinal frame beam under tabletop connecting pedestals
        MeshBuilder.add_box(bm, (0, 0, h - 0.05), (0.08, length * 0.85, 0.06), m_frame, "center_spine")

        # 2. Tabletop Slab
        top_th = 0.04
        MeshBuilder.add_box(bm, (0, 0, h - top_th / 2), (w, length, top_th), m_top, "tabletop")
        # Beveled edge rim
        MeshBuilder.add_box(bm, (0, 0, h - top_th / 2 - 0.01), (w + 0.02, length + 0.02, 0.015), m_steel, "table_edge_trim")

        # 3. Swivel Stools attached via curved swing arms
        stools_count = config.stool_count
        pairs = stools_count // 2
        y_step = length / (pairs + 1)
        stool_r = 0.16
        stool_h = 0.46

        for i in range(pairs):
            sy = -length / 2 + (i + 1) * y_step
            # Left and right side
            for side_sign in (-1, 1):
                # Swing arm angle
                arm_angle = 0.0
                if config.stool_swing_state == "random_pulled":
                    arm_angle = random.uniform(-0.35, 0.35)
                elif config.stool_swing_state == "scattered":
                    arm_angle = random.uniform(-0.65, 0.65)

                dist_out = (w / 2) + 0.22
                stool_x = dist_out * side_sign
                stool_y = sy + (arm_angle * 0.25)

                # Swing arm pipe from pedestal spine to stool base
                arm_start = Vector((0, sy, 0.22))
                arm_elbow = Vector((stool_x * 0.6, sy, 0.22))
                arm_end = Vector((stool_x, stool_y, 0.22))
                MeshBuilder.add_extruded_cable(bm, [arm_start, arm_elbow, arm_end], radius=0.022, sides=4, mat_idx=m_steel, name="stool_arm")

                # Vertical stool pedestal stem
                MeshBuilder.add_cylinder(bm, (stool_x, stool_y, stool_h / 2), 0.025, stool_h, sides=6, mat_idx=m_steel, name="stool_stem")
                # Round stool seat disc
                MeshBuilder.add_cylinder(bm, (stool_x, stool_y, stool_h + 0.025), stool_r, 0.05, sides=8, mat_idx=m_stool, name="stool_seat")

        # 4. Abandoned Mess Hall Food Trays & Cups
        if config.has_mess_trays:
            tray_positions = [(-w * 0.22, -0.30), (w * 0.22, 0.35)]
            for tx, ty in tray_positions:
                MeshBuilder.add_box(bm, (tx, ty, h + 0.015), (0.28, 0.38, 0.02), m_tray, "mess_tray")
                # Tin mug
                MeshBuilder.add_cylinder(bm, (tx + 0.08, ty + 0.10, h + 0.06), 0.035, 0.09, sides=6, mat_idx=m_steel, name="tin_mug")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
