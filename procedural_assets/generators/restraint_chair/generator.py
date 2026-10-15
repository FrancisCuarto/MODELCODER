import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import RestraintChairConfig

class RestraintChairGenerator(BaseGenerator):
    """Generates PS1 industrial heavy restraint chairs with shackles, straps, and IV poles."""

    def generate(self, config: RestraintChairConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_frame = mat_mgr.get_material_index("casing")
        m_pad = mat_mgr.get_material_index("chair_vinyl")
        m_strap = mat_mgr.get_material_index("casing_red")
        m_glass = mat_mgr.get_material_index("glass_tube")

        seat_z = 0.48
        seat_w = w * 0.72
        seat_d = d * 0.65

        # 1. Floor mounting base plate
        if config.floor_mounting_plate:
            plate_w = w * 0.90
            plate_d = d * 0.85
            MeshBuilder.add_box(bm, (0, 0, 0.015), (plate_w, plate_d, 0.03), m_steel, "floor_base_plate")
            # 4 Corner anchor bolts
            for bx in (-plate_w * 0.42, plate_w * 0.42):
                for by in (-plate_d * 0.42, plate_d * 0.42):
                    MeshBuilder.add_cylinder(bm, (bx, by, 0.035), 0.02, 0.04, sides=6, mat_idx=m_frame, name="anchor_bolt")

        # 2. Main welded square tube frame & 4 legs
        leg_th = 0.045
        leg_x = (seat_w / 2) - 0.03
        leg_y_front = (seat_d / 2) - 0.03
        leg_y_rear = -(seat_d / 2) + 0.03

        # Front legs
        for lx in (-leg_x, leg_x):
            MeshBuilder.add_box(bm, (lx, leg_y_front, seat_z / 2), (leg_th, leg_th, seat_z), m_frame, "front_leg")
            # Ankle shackles on front legs
            if config.leg_shackles:
                MeshBuilder.add_box(bm, (lx, leg_y_front + 0.04, 0.12), (0.09, 0.03, 0.05), m_steel, "ankle_cuff")
                MeshBuilder.add_cylinder(bm, (lx, leg_y_front + 0.04, 0.14), 0.012, 0.06, sides=4, mat_idx=m_steel, name="shackle_pin")

        # Rear upright posts (extending all the way up for the backrest)
        back_h = h - seat_z
        for lx in (-leg_x, leg_x):
            MeshBuilder.add_box(bm, (lx, leg_y_rear, h / 2), (leg_th, leg_th, h), m_frame, "rear_upright")

        # Frame crossbraces
        MeshBuilder.add_box(bm, (0, 0, seat_z - 0.04), (seat_w, seat_d, 0.04), m_frame, "seat_cradle")
        MeshBuilder.add_box(bm, (0, leg_y_rear, seat_z + back_h * 0.5), (seat_w, 0.04, 0.04), m_frame, "back_crossbar")

        # 3. Vinyl Padded Seat & Backrest
        MeshBuilder.add_box(bm, (0, 0, seat_z + 0.035), (seat_w - 0.02, seat_d - 0.02, 0.07), m_pad, "seat_cushion")

        # Backrest cushion
        back_cushion_h = back_h * 0.70
        back_cushion_z = seat_z + 0.07 + back_cushion_h / 2
        MeshBuilder.add_box(bm, (0, leg_y_rear + 0.035, back_cushion_z), (seat_w - 0.04, 0.06, back_cushion_h), m_pad, "back_cushion")

        # Headrest block
        if config.headrest_restraint:
            head_z = h - 0.08
            MeshBuilder.add_box(bm, (0, leg_y_rear + 0.035, head_z), (seat_w * 0.55, 0.07, 0.15), m_pad, "headrest_cushion")
            # Forehead restraint strap
            MeshBuilder.add_box(bm, (0, leg_y_rear + 0.075, head_z), (seat_w * 0.58, 0.02, 0.04), m_strap, "forehead_strap")

        # 4. Heavy Armrests with Wrist Straps
        arm_h = seat_z + 0.22
        arm_w = 0.08
        arm_l = seat_d * 0.90
        for ax in (-w / 2 + arm_w / 2, w / 2 - arm_w / 2):
            # Armrest support stanchions
            MeshBuilder.add_box(bm, (ax, 0, (seat_z + arm_h) / 2), (0.04, 0.04, arm_h - seat_z), m_frame, "arm_stanchion")
            # Armrest pad surface
            MeshBuilder.add_box(bm, (ax, 0.02, arm_h), (arm_w, arm_l, 0.04), m_steel, "armrest_pad")

            # Wrist restraint cuffs
            cuff_y = arm_l * 0.30
            if config.arm_straps == "buckled":
                MeshBuilder.add_box(bm, (ax, cuff_y, arm_h + 0.03), (arm_w + 0.02, 0.05, 0.02), m_strap, "wrist_cuff")
                MeshBuilder.add_box(bm, (ax, cuff_y, arm_h + 0.04), (0.04, 0.04, 0.015), m_steel, "cuff_buckle")
            elif config.arm_straps == "torn":
                MeshBuilder.add_box(bm, (ax - 0.02, cuff_y, arm_h + 0.02), (arm_w * 0.6, 0.04, 0.015), m_strap, "wrist_cuff_torn")
                MeshBuilder.add_box(bm, (ax + 0.04, cuff_y, arm_h - 0.05), (0.015, 0.04, 0.12), m_strap, "cuff_hanging")
            else: # loose
                MeshBuilder.add_box(bm, (ax + 0.03, cuff_y, arm_h + 0.01), (arm_w, 0.04, 0.015), m_strap, "cuff_loose")

        # 5. Attached Rear IV Infusion Drip Pole
        if config.iv_pole:
            pole_x = leg_x + 0.06
            pole_y = leg_y_rear - 0.04
            pole_h = h + 0.65
            MeshBuilder.add_cylinder(bm, (pole_x, pole_y, pole_h / 2), 0.015, pole_h, sides=6, mat_idx=m_steel, name="iv_pole_stem")
            # Top cross hook
            MeshBuilder.add_box(bm, (pole_x, pole_y, pole_h - 0.02), (0.22, 0.015, 0.015), m_steel, "iv_hook_arm")
            # Glass infusion flask hanging
            MeshBuilder.add_cylinder(bm, (pole_x + 0.08, pole_y, pole_h - 0.14), 0.04, 0.14, sides=6, mat_idx=m_glass, name="iv_flask")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
