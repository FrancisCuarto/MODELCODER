import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import SafetyShowerConfig

class SafetyShowerGenerator(BaseGenerator):
    """Generates emergency decontamination drench showers with eyewash basins and pull chains."""

    def generate(self, config: SafetyShowerConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_yellow = mat_mgr.get_material_index("hazard_yellow")
        m_steel = mat_mgr.get_material_index("mounting")
        m_frame = mat_mgr.get_material_index("casing")
        m_grate = mat_mgr.get_material_index("floor_grate" if "floor_grate" in mat_mgr.palette else "vent")
        m_valve = mat_mgr.get_material_index("valve_red")

        # 1. Floor Catch Basin & Drain Grate
        if config.has_floor_drain_grate:
            basin_w = w * 0.85
            basin_d = d * 0.85
            basin_h = 0.04
            # Outer rim
            MeshBuilder.add_box(bm, (0, 0, basin_h / 2), (basin_w, basin_d, basin_h), m_yellow, "drain_basin_rim")
            # Inner grated center
            MeshBuilder.add_box(bm, (0, 0, basin_h), (basin_w - 0.08, basin_d - 0.08, 0.005), m_grate, "drain_grate")

        # 2. Main Vertical Supply Riser Pipe (Safety Yellow)
        pipe_r = 0.032
        pipe_y = -(d / 2) + 0.12
        pipe_h = h - 0.15

        # Floor mounting flange
        MeshBuilder.add_cylinder(bm, (0, pipe_y, 0.02), pipe_r + 0.05, 0.04, sides=6, mat_idx=m_frame, name="base_flange")
        # Main upright pipe
        MeshBuilder.add_cylinder(bm, (0, pipe_y, pipe_h / 2), pipe_r, pipe_h, sides=6, mat_idx=m_yellow, name="main_riser_pipe")

        # Wall clamp bracket
        MeshBuilder.add_box(bm, (0, pipe_y - 0.05, h * 0.65), (0.16, 0.08, 0.04), m_frame, "wall_clamp")

        # 3. Overhead Cantilever Arm & Deluge Shower Bell
        if config.shower_type in ("combined_shower_eyewash", "decon_station_curtain"):
            arm_z = h - 0.10
            shower_y = 0.05
            # Horizontal pipe arm extending forward over head
            p_start = Vector((0, pipe_y, arm_z))
            p_end = Vector((0, shower_y, arm_z))
            MeshBuilder.add_extruded_cable(bm, [p_start, p_end], radius=pipe_r * 0.85, sides=6, mat_idx=m_yellow, name="shower_arm")

            # Ball valve on pipe
            MeshBuilder.add_box(bm, (0, pipe_y + 0.12, arm_z), (0.07, 0.07, 0.07), m_steel, "shower_ball_valve")

            # Conical drench shower head
            MeshBuilder.add_cylinder(bm, (0, shower_y, arm_z - 0.06), 0.14, 0.08, sides=8, mat_idx=m_yellow, name="shower_bell")
            MeshBuilder.add_cylinder(bm, (0, shower_y, arm_z - 0.10), 0.12, 0.015, sides=8, mat_idx=m_steel, name="shower_spray_plate")

            # 4. Triangular Pull-Down Actuator Ring & Rod
            if config.has_pull_chain:
                rod_z_top = arm_z
                rod_len = 0.85
                rod_y = pipe_y + 0.12
                # Pull rod
                MeshBuilder.add_cylinder(bm, (0.06, rod_y, rod_z_top - rod_len / 2), 0.008, rod_len, sides=4, mat_idx=m_steel, name="pull_rod")
                # Triangular grip ring
                MeshBuilder.add_box(bm, (0.06, rod_y, rod_z_top - rod_len), (0.12, 0.015, 0.12), m_yellow, "pull_ring")

        # 5. Waist-Level Stainless Steel Eyewash Basin
        if config.has_eyewash_bowl:
            eye_z = 0.95
            eye_y = pipe_y + 0.22

            # Branch pipe from riser
            MeshBuilder.add_cylinder(bm, (0, pipe_y + 0.10, eye_z - 0.05), 0.02, 0.20, sides=4, axis='Y', mat_idx=m_yellow, name="eyewash_branch")

            # Circular stainless bowl
            MeshBuilder.add_cylinder(bm, (0, eye_y, eye_z), 0.16, 0.08, sides=8, mat_idx=m_steel, name="eyewash_bowl")

            # Twin upward spray aerator nozzles
            for nx in (-0.05, 0.05):
                MeshBuilder.add_cylinder(bm, (nx, eye_y, eye_z + 0.04), 0.016, 0.04, sides=4, mat_idx=m_steel, name="spray_nozzle")
                MeshBuilder.add_cylinder(bm, (nx, eye_y, eye_z + 0.06), 0.018, 0.01, sides=4, mat_idx=m_yellow, name="nozzle_cap")

            # Large yellow hand push-flag activator lever
            MeshBuilder.add_box(bm, (0.18, eye_y, eye_z + 0.02), (0.015, 0.12, 0.10), m_yellow, "push_flag_lever")

        # 6. High-Visibility Emergency Sign
        if config.has_hazard_stripes:
            MeshBuilder.add_box(bm, (0, pipe_y + 0.04, h - 0.35), (0.24, 0.01, 0.24), m_yellow, "safety_sign_board")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
