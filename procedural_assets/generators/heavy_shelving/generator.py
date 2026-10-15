import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import HeavyShelvingConfig

class HeavyShelvingGenerator(BaseGenerator):
    """Generates industrial slotted angle-iron warehouse shelving racks with cargo boxes and canisters."""

    def generate(self, config: HeavyShelvingConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_frame = mat_mgr.get_material_index("casing")
        m_steel = mat_mgr.get_material_index("mounting")
        m_shelf = mat_mgr.get_material_index("locker_gray")
        m_crate = mat_mgr.get_material_index("hazard_yellow")
        m_drum = mat_mgr.get_material_index("chemical_barrel_blue")

        # 1. Four Upright Slotted Angle-Iron Corner Posts
        post_th = 0.045
        post_x = (w / 2) - post_th / 2
        post_y = (d / 2) - post_th / 2

        for px in (-post_x, post_x):
            for py in (-post_y, post_y):
                MeshBuilder.add_box(bm, (px, py, h / 2), (post_th, post_th, h), m_frame, "corner_post")
                # Base foot bracket
                MeshBuilder.add_box(bm, (px, py, 0.015), (post_th + 0.03, post_th + 0.03, 0.03), m_steel, "post_foot")

        # Side horizontal tie-bars
        for py in (-post_y, post_y):
            pass # (covered by shelf beams)

        # 2. Horizontal Shelf Tiers
        levels = config.levels
        bottom_gap = 0.15
        shelf_spacing = (h - bottom_gap - 0.10) / max(1, levels - 1)

        shelf_z_list = []
        for lv in range(levels):
            sz = bottom_gap + (lv * shelf_spacing)
            shelf_z_list.append(sz)

            # Check if this shelf is warped/bent
            is_bent = (config.bent_shelf_index == lv)

            # Front & rear support beams
            MeshBuilder.add_box(bm, (0, -post_y, sz - 0.02), (w, 0.03, 0.04), m_frame, f"shelf_beam_front_{lv}")
            MeshBuilder.add_box(bm, (0, post_y, sz - 0.02), (w, 0.03, 0.04), m_frame, f"shelf_beam_rear_{lv}")
            # Left & right side beams
            MeshBuilder.add_box(bm, (-post_x, 0, sz - 0.02), (0.03, d - post_th * 2, 0.04), m_frame, f"shelf_beam_L_{lv}")
            MeshBuilder.add_box(bm, (post_x, 0, sz - 0.02), (0.03, d - post_th * 2, 0.04), m_frame, f"shelf_beam_R_{lv}")

            # Shelf board plank
            board_th = 0.025
            if is_bent:
                # Drooping bent shelf in center
                MeshBuilder.add_box(bm, (0, 0, sz - 0.03), (w - 0.06, d - 0.06, board_th), m_shelf, f"shelf_board_bent_{lv}")
            else:
                MeshBuilder.add_box(bm, (0, 0, sz + board_th / 2), (w - 0.06, d - 0.06, board_th), m_shelf, f"shelf_board_{lv}")

            # Front retaining crossbar (seismic / zero-G retainer)
            if config.has_retaining_bars and lv > 0:
                MeshBuilder.add_cylinder(bm, (0, post_y + 0.01, sz + 0.10), 0.008, w - 0.04, sides=4, axis='X', mat_idx=m_steel, name=f"retainer_{lv}")

            # 3. Cargo items placed on shelves
            if config.shelf_type == "cargo_storage" and lv < levels - 1:
                # Add supply boxes on shelf
                if random.random() < 0.75:
                    bx1_w, bx1_h, bx1_d = 0.28, 0.24, 0.35
                    MeshBuilder.add_box(bm, (-w * 0.24, 0, sz + board_th + bx1_h / 2), (bx1_w, bx1_d, bx1_h), m_crate, "cargo_box_1")
                if random.random() < 0.70:
                    bx2_w, bx2_h, bx2_d = 0.22, 0.20, 0.30
                    MeshBuilder.add_box(bm, (w * 0.20, 0, sz + board_th + bx2_h / 2), (bx2_w, bx2_d, bx2_h), m_steel, "cargo_box_2")

            elif config.shelf_type == "chemical_drums_rack" and lv == 0:
                # Heavy drums on lowest reinforced shelf
                for dx in (-w * 0.25, w * 0.25):
                    drum_r = 0.16
                    drum_h = 0.42
                    MeshBuilder.add_cylinder(bm, (dx, 0, sz + board_th + drum_h / 2), drum_r, drum_h, sides=8, mat_idx=m_drum, name="chem_drum")

        # 4. Rear Diagonal X-Bracing Wire Struts
        if config.has_x_bracing:
            rear_y = -post_y
            wire_r = 0.008
            p_bot_L = Vector((-post_x, rear_y, bottom_gap))
            p_top_R = Vector((post_x, rear_y, h - 0.10))
            p_bot_R = Vector((post_x, rear_y, bottom_gap))
            p_top_L = Vector((-post_x, rear_y, h - 0.10))

            MeshBuilder.add_extruded_cable(bm, [p_bot_L, p_top_R], radius=wire_r, sides=4, mat_idx=m_steel, name="x_brace_1")
            MeshBuilder.add_extruded_cable(bm, [p_bot_R, p_top_L], radius=wire_r, sides=4, mat_idx=m_steel, name="x_brace_2")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
