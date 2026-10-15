import random
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import MedicalScreenConfig

class MedicalScreenGenerator(BaseGenerator):
    """Generates folding tubular medical privacy screens with vinyl dividers and casters."""

    def generate(self, config: MedicalScreenConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        n_panels = config.panel_count
        if config.screen_type == "single_partition":
            n_panels = 1
        elif config.screen_type == "four_panel":
            n_panels = 4
        elif config.screen_type == "three_panel":
            n_panels = 3

        pw = config.panel_width
        ph = config.panel_height
        fold_angle = math.radians(config.fold_angle_deg)

        m_tube = mat_mgr.get_material_index("mounting")
        m_sheet = mat_mgr.get_material_index("chair_vinyl")
        m_wheel = mat_mgr.get_material_index("rubber_tire")
        m_blood = mat_mgr.get_material_index("rust_patch")

        tube_r = 0.016
        post_h = ph
        curtain_bottom_z = 0.25
        curtain_top_z = ph - 0.08
        curtain_h = curtain_top_z - curtain_bottom_z

        # Calculate panel sequence with alternating fold angles
        current_x = -((n_panels * pw * math.cos(fold_angle)) / 2)
        current_y = 0.0

        for i in range(n_panels):
            # Alternating direction: panel 0 angles +fold, panel 1 angles -fold, etc.
            sign = 1 if (i % 2 == 0) else -1
            angle = fold_angle * sign if n_panels > 1 else 0.0

            dx = pw * math.cos(angle)
            dy = pw * math.sin(angle)

            p_start = Vector((current_x, current_y, 0))
            p_end = Vector((current_x + dx, current_y + dy, 0))
            p_mid = (p_start + p_end) / 2

            # Left upright post
            MeshBuilder.add_cylinder(bm, (p_start.x, p_start.y, post_h / 2), tube_r, post_h, sides=6, mat_idx=m_tube, name=f"post_{i}_L")

            # Right upright post (for the last panel, or hinge connection)
            if i == n_panels - 1:
                MeshBuilder.add_cylinder(bm, (p_end.x, p_end.y, post_h / 2), tube_r, post_h, sides=6, mat_idx=m_tube, name=f"post_{i}_R")

            # Top horizontal crossbar
            top_bar_pts = [Vector((p_start.x, p_start.y, curtain_top_z)), Vector((p_end.x, p_end.y, curtain_top_z))]
            MeshBuilder.add_extruded_cable(bm, top_bar_pts, radius=tube_r, sides=4, mat_idx=m_tube, name=f"top_bar_{i}")

            # Bottom horizontal crossbar
            bot_bar_pts = [Vector((p_start.x, p_start.y, curtain_bottom_z)), Vector((p_end.x, p_end.y, curtain_bottom_z))]
            MeshBuilder.add_extruded_cable(bm, bot_bar_pts, radius=tube_r, sides=4, mat_idx=m_tube, name=f"bot_bar_{i}")

            # Caster wheels on start post (and end post if last)
            if config.caster_wheels:
                MeshBuilder.add_cylinder(bm, (p_start.x, p_start.y, 0.05), 0.03, 0.06, sides=6, mat_idx=m_wheel, name=f"wheel_{i}_L")
                if i == n_panels - 1:
                    MeshBuilder.add_cylinder(bm, (p_end.x, p_end.y, 0.05), 0.03, 0.06, sides=6, mat_idx=m_wheel, name=f"wheel_{i}_R")

            # Curtain panel sheet
            sheet_mat = m_sheet
            if config.curtain_damage == "blood_splatter" and i == 1:
                sheet_mat = m_blood

            # Calculate box rotation or oriented sheet
            c_center = (p_start + p_end) / 2
            c_center.z = (curtain_top_z + curtain_bottom_z) / 2

            # Use low poly box oriented along panel
            sheet_len = pw - (tube_r * 2)
            sheet_thick = 0.012

            # If torn hanging on middle panel
            if config.curtain_damage == "torn_hanging" and i == 1:
                # Partial drooping curtain
                half_len = sheet_len * 0.70
                half_h = curtain_h * 0.65
                h_center = Vector((p_start.x + (dx * 0.35), p_start.y + (dy * 0.35), curtain_bottom_z + half_h / 2))
                rot_mat = Matrix.Rotation(angle, 4, 'Z')
                box_verts = MeshBuilder.add_box(bm, (0, 0, 0), (half_len, sheet_thick, half_h), sheet_mat, f"curtain_torn_{i}")
                # Transform verts to oriented position
                for v in bm.verts:
                    if v.select:
                        v.co = rot_mat @ v.co + h_center
            else:
                rot_mat = Matrix.Rotation(angle, 4, 'Z')
                MeshBuilder.add_box(bm, (0, 0, 0), (sheet_len, sheet_thick, curtain_h), sheet_mat, f"curtain_{i}")
                for v in bm.verts:
                    if v.select:
                        v.co = rot_mat @ v.co + c_center

            # Update coordinates for next panel
            current_x += dx
            current_y += dy

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
