import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import SpaceToiletConfig

class SpaceToiletGenerator(BaseGenerator):
    """Generates space station vacuum latrines with stainless steel bowls and zero-g restraints."""

    def generate(self, config: SpaceToiletConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_casing = mat_mgr.get_material_index("casing")
        m_pad = mat_mgr.get_material_index("rubber_tire")
        m_pipe = mat_mgr.get_material_index("pipe_industrial")
        m_paper = mat_mgr.get_material_index("gauge")

        # 1. Rear Wall-Mount Tank / Valve Shroud
        tank_w = w * 0.90
        tank_d = d * 0.32
        tank_h = h
        tank_y = -(d / 2) + tank_d / 2
        MeshBuilder.add_box(bm, (0, tank_y, tank_h / 2), (tank_w, tank_d, tank_h), m_casing, "rear_shroud")

        # Manual vacuum flush lever / pedal
        MeshBuilder.add_box(bm, (w / 2 - 0.08, tank_y + tank_d / 2 + 0.03, 0.12), (0.05, 0.10, 0.03), m_steel, "flush_pedal")

        # 2. Main Stainless Steel Conical Bowl Pedestal
        bowl_h = 0.46
        bowl_y = 0.08
        bowl_r_top = w * 0.44
        bowl_r_bot = w * 0.32

        # Base column
        MeshBuilder.add_cylinder(bm, (0, bowl_y, bowl_h / 2), bowl_r_bot, bowl_h, sides=8, mat_idx=m_steel, name="bowl_base_column")
        # Upper flared bowl rim
        MeshBuilder.add_cylinder(bm, (0, bowl_y, bowl_h - 0.03), bowl_r_top, 0.08, sides=8, mat_idx=m_steel, name="bowl_rim")

        # 3. Hinged Toilet Seat & Seal Lid
        lid_z = bowl_h + 0.03
        lid_th = 0.035
        seat_w = w * 0.88
        seat_d = d * 0.60

        if config.lid_state == "closed":
            # Flat closed sealed lid
            MeshBuilder.add_box(bm, (0, bowl_y, lid_z), (seat_w, seat_d, lid_th), m_casing, "toilet_lid_closed")
            # Rubber perimeter seal gasket
            MeshBuilder.add_box(bm, (0, bowl_y, lid_z - 0.015), (seat_w - 0.02, seat_d - 0.02, 0.01), m_pad, "gasket_seal")
        elif config.lid_state == "open":
            # Seat ring down
            MeshBuilder.add_box(bm, (0, bowl_y, lid_z), (seat_w, seat_d, 0.025), m_pad, "seat_ring")
            # Lid tilted back against tank
            MeshBuilder.add_box(bm, (0, tank_y + tank_d / 2 + 0.02, bowl_h + seat_d * 0.45), (seat_w, 0.03, seat_d * 0.90), m_casing, "toilet_lid_open")
        else: # damaged
            # Ajar tilted cracked lid
            MeshBuilder.add_box(bm, (0.04, bowl_y - 0.02, lid_z + 0.05), (seat_w * 0.85, seat_d * 0.85, 0.03), m_casing, "toilet_lid_broken")

        # 4. Zero-G Padded Thigh Restraint Clamp Handles
        if config.has_thigh_restraints:
            rest_h = bowl_h + 0.22
            tube_r = 0.018
            for rx in (-w / 2 - 0.02, w / 2 + 0.02):
                # Vertical mounting stalk
                MeshBuilder.add_cylinder(bm, (rx, bowl_y, rest_h / 2), tube_r, rest_h, sides=4, mat_idx=m_steel, name="restraint_stalk")
                # Curved horizontal thigh clamp pad
                MeshBuilder.add_box(bm, (rx, bowl_y + 0.04, rest_h), (0.06, 0.22, 0.05), m_pad, "thigh_clamp_pad")

        # 5. Vacuum Suction Waste Conduit Pipe
        if config.vacuum_pipe:
            p_start = Vector((0, bowl_y, 0.15))
            p_end = Vector((0, tank_y, 0.22))
            MeshBuilder.add_extruded_cable(bm, [p_start, p_end], radius=0.035, sides=6, mat_idx=m_pipe, name="vacuum_waste_pipe")

        # 6. Wall-Mounted Toilet Paper Dispenser Box
        if config.has_paper_dispenser:
            box_x = (w / 2) + 0.10
            box_y = tank_y + 0.06
            box_z = bowl_h + 0.25
            MeshBuilder.add_box(bm, (box_x, box_y, box_z), (0.10, 0.16, 0.16), m_steel, "paper_dispenser_box")
            MeshBuilder.add_box(bm, (box_x, box_y, box_z - 0.07), (0.06, 0.08, 0.03), m_paper, "paper_roll_tail")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
