import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import ToolChestCartConfig

class ToolChestCartGenerator(BaseGenerator):
    """Generates heavy mobile mechanic tool chests with red/yellow powder-coat and drawer slides."""

    def generate(self, config: ToolChestCartConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_red = mat_mgr.get_material_index("casing_red")
        m_body = mat_mgr.get_material_index("casing")
        m_steel = mat_mgr.get_material_index("mounting")
        m_wheel = mat_mgr.get_material_index("rubber_tire")
        m_part = mat_mgr.get_material_index("switch_metal")

        # 1. 4 Heavy Duty Rubber Swivel Casters
        wheel_r = 0.05
        wheel_w = 0.035
        base_z = 0.08
        x_wheel = (w / 2) - 0.06
        y_wheel = (d / 2) - 0.06

        for wx in (-x_wheel, x_wheel):
            for wy in (-y_wheel, y_wheel):
                MeshBuilder.add_cylinder(bm, (wx, wy, wheel_r), wheel_r, wheel_w, sides=6, axis='X', mat_idx=m_wheel, name="caster")
                MeshBuilder.add_cylinder(bm, (wx, wy, wheel_r + 0.03), 0.016, 0.04, sides=4, mat_idx=m_steel, name="stem")

        # 2. Main Tool Chest Cabinet Box
        cab_h = h - base_z - 0.04
        cab_z = base_z + cab_h / 2
        MeshBuilder.add_box(bm, (0, 0, cab_z), (w, d, cab_h), m_red, "tool_chest_body")

        # Protective bumper corner trims
        corner_w = 0.03
        for cx in (-w / 2 + corner_w / 2, w / 2 - corner_w / 2):
            for cy in (-d / 2 + corner_w / 2, d / 2 - corner_w / 2):
                MeshBuilder.add_box(bm, (cx, cy, cab_z), (corner_w + 0.01, corner_w + 0.01, cab_h), m_body, "bumper_corner")

        # 3. Top Recessed Work Tray with Rubber Mat
        top_z = h - 0.02
        tray_lip = 0.035
        # Top lip
        MeshBuilder.add_box(bm, (0, 0, top_z), (w + 0.02, d + 0.02, 0.03), m_body, "tray_lip_rim")
        # Inset black rubber mat
        MeshBuilder.add_box(bm, (0, 0, top_z + 0.01), (w - 0.04, d - 0.04, 0.005), m_wheel, "rubber_mat")

        # Loose mechanical spare parts on top mat
        if config.has_top_mat_parts:
            MeshBuilder.add_cylinder(bm, (-0.12, 0.05, top_z + 0.03), 0.03, 0.04, sides=6, mat_idx=m_part, name="bearing")
            MeshBuilder.add_box(bm, (0.10, -0.06, top_z + 0.02), (0.05, 0.08, 0.025), m_steel, "bracket_spare")

        # 4. Side Tubular Push Handle
        if config.has_side_handle:
            hx = (w / 2) + 0.06
            hz = h - 0.12
            # Standoff brackets
            MeshBuilder.add_box(bm, ((w / 2) + 0.03, -d * 0.25, hz), (0.06, 0.03, 0.03), m_steel, "handle_bracket_1")
            MeshBuilder.add_box(bm, ((w / 2) + 0.03, d * 0.25, hz), (0.06, 0.03, 0.03), m_steel, "handle_bracket_2")
            # Grip bar
            MeshBuilder.add_cylinder(bm, (hx, 0, hz), 0.016, d * 0.60, sides=6, axis='Y', mat_idx=m_steel, name="push_handle_bar")

        # 5. Sliding Drawers Stack
        drawer_n = config.drawer_count
        drawer_gap = 0.012
        drawer_h = (cab_h - 0.08 - (drawer_n * drawer_gap)) / drawer_n
        drawer_w = w - 0.10
        front_y = d / 2

        for i in range(drawer_n):
            dz = base_z + 0.05 + i * (drawer_h + drawer_gap) + drawer_h / 2

            # Open drawer offset
            y_ext = 0.0
            if config.drawer_open_style == "top_drawer_open" and i == drawer_n - 1:
                y_ext = d * 0.35
            elif config.drawer_open_style == "staggered":
                if i == drawer_n - 1:
                    y_ext = d * 0.35
                elif i == drawer_n - 2:
                    y_ext = d * 0.18

            # Drawer front face
            MeshBuilder.add_box(bm, (0, front_y + y_ext, dz), (drawer_w, 0.025, drawer_h), m_red, f"drawer_front_{i}")

            # Drawer interior if open
            if y_ext > 0.03:
                MeshBuilder.add_box(bm, (0, front_y + y_ext / 2, dz - 0.01), (drawer_w - 0.04, y_ext, drawer_h - 0.03), m_body, f"drawer_box_{i}")

            # Full-width brushed aluminum handle trim
            MeshBuilder.add_box(bm, (0, front_y + y_ext + 0.015, dz + drawer_h * 0.28), (drawer_w - 0.02, 0.015, 0.02), m_steel, f"handle_trim_{i}")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
