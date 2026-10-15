import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import WorkBenchConfig

class WorkBenchGenerator(BaseGenerator):
    """Generates heavy maintenance workbenches with vises, pegboards, and overhead lights."""

    def generate(self, config: WorkBenchConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_frame = mat_mgr.get_material_index("casing")
        m_steel = mat_mgr.get_material_index("mounting")
        m_wood = mat_mgr.get_material_index("locker_gray")
        m_lamp = mat_mgr.get_material_index("fluorescent_tube_lit")
        m_tool = mat_mgr.get_material_index("switch_metal")

        # 1. Heavy Legs & Lower Chassis
        leg_th = 0.06
        leg_x = (w / 2) - 0.08
        leg_y = (d / 2) - 0.08
        leg_h = h - 0.06

        for lx in (-leg_x, leg_x):
            for ly in (-leg_y, leg_y):
                MeshBuilder.add_box(bm, (lx, ly, leg_h / 2), (leg_th, leg_th, leg_h), m_frame, "leg")
                # Foot pad
                MeshBuilder.add_box(bm, (lx, ly, 0.02), (leg_th + 0.04, leg_th + 0.04, 0.04), m_steel, "foot")

        # Lower frame crossbars
        MeshBuilder.add_box(bm, (0, -leg_y, 0.18), (w - 0.16, 0.04, 0.05), m_frame, "cross_front")
        MeshBuilder.add_box(bm, (0, leg_y, 0.18), (w - 0.16, 0.04, 0.05), m_frame, "cross_rear")
        MeshBuilder.add_box(bm, (-leg_x, 0, 0.18), (0.04, d - 0.16, 0.05), m_frame, "cross_L")
        MeshBuilder.add_box(bm, (leg_x, 0, 0.18), (0.04, d - 0.16, 0.05), m_frame, "cross_R")

        # Lower storage shelf
        if config.has_under_shelf:
            MeshBuilder.add_box(bm, (0, 0, 0.20), (w - 0.14, d - 0.14, 0.03), m_steel, "under_shelf")

        # 2. Main Worktop Slab
        top_th = 0.07
        top_z = h - top_th / 2
        MeshBuilder.add_box(bm, (0, 0, top_z), (w, d, top_th), m_wood, "worktop")
        # Metal edge surround
        MeshBuilder.add_box(bm, (0, 0, top_z), (w + 0.02, d + 0.02, 0.02), m_steel, "top_trim")

        # 3. Heavy Bench Vise (attached on front-right corner)
        if config.has_vise:
            vx = (w / 2) - 0.18
            vy = (d / 2) - 0.08
            vz = h + 0.08
            # Vise base swivel mount
            MeshBuilder.add_cylinder(bm, (vx, vy, h + 0.02), 0.08, 0.04, sides=6, mat_idx=m_frame, name="vise_base")
            # Fixed jaw body
            MeshBuilder.add_box(bm, (vx, vy - 0.03, vz), (0.12, 0.10, 0.09), m_frame, "vise_fixed_jaw")
            # Sliding jaw
            MeshBuilder.add_box(bm, (vx, vy + 0.05, vz), (0.12, 0.06, 0.09), m_steel, "vise_slide_jaw")
            # Screw bar & turn handle
            MeshBuilder.add_cylinder(bm, (vx, vy + 0.10, vz), 0.015, 0.18, sides=4, axis='Y', mat_idx=m_tool, name="vise_screw")
            MeshBuilder.add_cylinder(bm, (vx, vy + 0.19, vz), 0.012, 0.16, sides=4, axis='Z', mat_idx=m_tool, name="vise_handle")

        # 4. Rear Upright Pegboard with Hanging Tool Silhouettes
        if config.has_pegboard:
            peg_h = 0.85
            peg_z = h + peg_h / 2
            peg_y = -(d / 2) + 0.02
            # Pegboard panel
            MeshBuilder.add_box(bm, (0, peg_y, peg_z), (w - 0.04, 0.025, peg_h), m_frame, "pegboard_panel")

            # Hanging tool representations (wrench, hammer, hacksaw)
            # Wrench
            MeshBuilder.add_box(bm, (-w * 0.25, peg_y + 0.02, peg_z + 0.15), (0.04, 0.015, 0.24), m_tool, "wrench_tool")
            # Heavy hammer
            MeshBuilder.add_box(bm, (-w * 0.10, peg_y + 0.02, peg_z + 0.10), (0.03, 0.015, 0.28), m_tool, "hammer_shaft")
            MeshBuilder.add_box(bm, (-w * 0.10, peg_y + 0.025, peg_z + 0.22), (0.10, 0.03, 0.05), m_steel, "hammer_head")

        # 5. Cantilevered Overhead Task Luminaire
        if config.has_overhead_light and config.has_pegboard:
            light_h = h + peg_h + 0.15
            lamp_y = -(d / 2) + (d * 0.40)
            # Twin support arm stalks
            for arm_x in (-w * 0.35, w * 0.35):
                # Vertical extension
                MeshBuilder.add_cylinder(bm, (arm_x, -(d / 2) + 0.02, light_h - 0.10), 0.018, 0.28, sides=4, mat_idx=m_frame, name="light_stalk")
                # Forward cantilever
                MeshBuilder.add_box(bm, (arm_x, -(d / 4), light_h), (0.025, d * 0.45, 0.025), m_frame, "light_arm")

            # Overhead fluorescent fixture
            MeshBuilder.add_box(bm, (0, 0, light_h), (w * 0.70, 0.14, 0.04), m_frame, "luminaire_chassis")
            MeshBuilder.add_cylinder(bm, (0, 0, light_h - 0.02), 0.02, w * 0.65, sides=6, axis='X', mat_idx=m_lamp, name="fluorescent_tube")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
