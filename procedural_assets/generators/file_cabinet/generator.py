import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import FileCabinetConfig

class FileCabinetGenerator(BaseGenerator):
    """Generates office metal filing cabinets with sliding drawers, label holders, and loose papers."""

    def generate(self, config: FileCabinetConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        h = config.height
        d = config.depth

        if config.cabinet_style == "lateral_wide":
            w = max(w, 0.95)
            h = min(h, 1.10)
        elif config.cabinet_style == "blueprint_flat_file":
            w = max(w, 1.15)
            d = max(d, 0.85)
            h = min(h, 0.85)

        m_body = mat_mgr.get_material_index("locker_gray")
        m_casing = mat_mgr.get_material_index("casing")
        m_handle = mat_mgr.get_material_index("mounting")
        m_paper = mat_mgr.get_material_index("gauge")

        # 1. Main outer casing shell
        base_h = 0.06
        cab_h = h - base_h
        cab_z = base_h + cab_h / 2

        # Recessed base plinth
        MeshBuilder.add_box(bm, (0, 0, base_h / 2), (w - 0.04, d - 0.04, base_h), m_casing, "base_plinth")
        # Main body box
        MeshBuilder.add_box(bm, (0, 0, cab_z), (w, d, cab_h), m_body, "casing_body")

        # Top key lock cylinder
        MeshBuilder.add_cylinder(bm, (w / 2 - 0.06, d / 2 + 0.005, h - 0.05), 0.015, 0.02, sides=6, axis='Y', mat_idx=m_handle, name="lock_cylinder")

        # 2. Drawers Stack
        drawer_n = config.drawer_count
        drawer_gap = 0.015
        total_gaps = (drawer_n + 1) * drawer_gap
        drawer_h = (cab_h - total_gaps - 0.06) / drawer_n
        drawer_w = w - 0.06
        front_y = d / 2

        for i in range(drawer_n):
            d_z = base_h + 0.04 + drawer_gap + i * (drawer_h + drawer_gap) + drawer_h / 2

            # Calculate open extension
            y_ext = 0.0
            if config.drawer_open_mode == "staggered_open":
                if i == drawer_n - 1: # Top drawer open
                    y_ext = d * 0.35
                elif i == drawer_n - 2:
                    y_ext = d * 0.15
            elif config.drawer_open_mode == "looted_papers":
                if i == drawer_n - 1:
                    y_ext = d * 0.45
                elif i == 0:
                    y_ext = d * 0.20

            d_center_y = front_y + y_ext

            # Drawer front face
            MeshBuilder.add_box(bm, (0, d_center_y, d_z), (drawer_w, 0.025, drawer_h), m_body, f"drawer_face_{i}")

            # Drawer box body (if pulled open)
            if y_ext > 0.03:
                box_d = y_ext
                MeshBuilder.add_box(bm, (0, front_y + y_ext / 2 - 0.01, d_z - 0.02), (drawer_w - 0.04, box_d, drawer_h - 0.04), m_casing, f"drawer_interior_{i}")

                # Hanging folders or spilled papers
                if config.drawer_open_mode == "looted_papers" and i == drawer_n - 1:
                    MeshBuilder.add_box(bm, (0.02, d_center_y - 0.05, d_z + drawer_h * 0.35), (drawer_w * 0.75, 0.02, 0.08), m_paper, "paper_folder_1")
                    MeshBuilder.add_box(bm, (-0.05, d_center_y + 0.02, d_z + drawer_h * 0.25), (0.16, 0.12, 0.01), m_paper, "spilled_sheet")

            # Drawer pull handle (horizontal recessed or arched bar)
            handle_z = d_z + drawer_h * 0.15
            MeshBuilder.add_box(bm, (0, d_center_y + 0.02, handle_z), (drawer_w * 0.35, 0.02, 0.03), m_handle, f"handle_{i}")

            # Metal index card / label holder frame
            if config.has_label_holders:
                label_z = d_z - drawer_h * 0.15
                MeshBuilder.add_box(bm, (0, d_center_y + 0.015, label_z), (0.10, 0.01, 0.05), m_handle, f"label_frame_{i}")
                MeshBuilder.add_box(bm, (0, d_center_y + 0.02, label_z), (0.08, 0.005, 0.035), m_paper, f"label_paper_{i}")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
