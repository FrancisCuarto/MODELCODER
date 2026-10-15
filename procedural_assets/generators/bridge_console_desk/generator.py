import random
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import BridgeConsoleDeskConfig

class BridgeConsoleDeskGenerator(BaseGenerator):
    """Generates complex retrofuturistic bridge command horseshoe consoles with CRTs and pilot chair."""

    def generate(self, config: BridgeConsoleDeskConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_body = mat_mgr.get_material_index("casing")
        m_panel = mat_mgr.get_material_index("locker_gray")
        m_steel = mat_mgr.get_material_index("mounting")
        m_crt = mat_mgr.get_material_index("crt_screen_green" if config.screen_color == "green" else "crt_screen_amber")
        m_guard = mat_mgr.get_material_index("button_red")
        m_chair = mat_mgr.get_material_index("chair_vinyl")

        # 1. Main Center Console Desk Block
        center_w = w * 0.55
        center_d = d * 0.45
        desk_h = 0.76
        center_y = d * 0.25

        # Base cabinet
        MeshBuilder.add_box(bm, (0, center_y, desk_h / 2), (center_w, center_d, desk_h), m_body, "center_desk_base")

        # Angled canopy housing holding CRTs (angled 30 degrees toward operator)
        canopy_h = h - desk_h
        canopy_d = center_d * 0.85
        canopy_z = desk_h + canopy_h / 2
        MeshBuilder.add_box(bm, (0, center_y + 0.05, canopy_z), (center_w, canopy_d, canopy_h), m_panel, "center_canopy")

        # Recessed Center CRT Screen
        crt_w = 0.38
        crt_h = 0.28
        MeshBuilder.add_box(bm, (0, center_y - canopy_d / 2 + 0.02, canopy_z), (crt_w, 0.02, crt_h), m_crt, "center_crt_screen")

        # 2. Left & Right Wraparound Wing Consoles (Angles creating the 'U' / horseshoe)
        wing_w = 0.45
        wing_len = d * 0.65
        wing_angle = math.radians(45.0)

        for side_sign in (-1, 1):
            wing_center_x = (center_w / 2 + 0.22) * side_sign
            wing_center_y = center_y - 0.25

            # Rotated side wing console
            rot_mat = Matrix.Rotation(wing_angle * (-side_sign), 4, 'Z')

            # Wing desk base
            wing_pos = Vector((wing_center_x, wing_center_y, desk_h / 2))
            MeshBuilder.add_box(bm, (0, 0, 0), (wing_w, wing_len, desk_h), m_body, f"wing_base_{side_sign}")
            for v in bm.verts:
                if v.select:
                    v.co = rot_mat @ v.co + wing_pos

            # Wing canopy & secondary CRT
            wing_canopy_pos = Vector((wing_center_x, wing_center_y, canopy_z))
            MeshBuilder.add_box(bm, (0, 0, 0), (wing_w - 0.04, wing_len * 0.85, canopy_h), m_panel, f"wing_canopy_{side_sign}")
            for v in bm.verts:
                if v.select:
                    v.co = rot_mat @ v.co + wing_canopy_pos

            # Secondary CRT monitor on side wings
            if config.crt_count >= 2:
                wing_crt_pos = Vector((wing_center_x, wing_center_y, canopy_z))
                MeshBuilder.add_box(bm, (0, 0.02, 0), (0.28, 0.02, 0.22), m_crt, f"wing_crt_{side_sign}")
                for v in bm.verts:
                    if v.select:
                        v.co = rot_mat @ v.co + wing_crt_pos

        # 3. Guarded Missile Breaker Switches (Toggle Guards)
        if config.has_toggle_guards:
            for gx in (-0.18, -0.10, 0.10, 0.18):
                # Red flip-up safety guard hood
                MeshBuilder.add_box(bm, (gx, center_y - center_d / 2 + 0.08, desk_h + 0.02), (0.035, 0.05, 0.025), m_guard, "missile_guard")
                # Metal toggle switch toggle
                MeshBuilder.add_cylinder(bm, (gx, center_y - center_d / 2 + 0.08, desk_h + 0.04), 0.006, 0.03, sides=4, mat_idx=m_steel, name="switch_stick")

        # 4. Gooseneck Communications Microphone Stalk
        if config.has_microphone_stalk:
            mic_base = Vector((-center_w * 0.35, center_y - center_d * 0.30, desk_h + 0.02))
            mic_tip = Vector((-center_w * 0.20, center_y - center_d * 0.45, desk_h + 0.22))
            MeshBuilder.add_extruded_cable(bm, [mic_base, mic_tip], radius=0.012, sides=4, mat_idx=m_steel, name="mic_stalk")
            MeshBuilder.add_cylinder(bm, (mic_tip.x, mic_tip.y, mic_tip.z), 0.02, 0.04, sides=6, mat_idx=m_body, name="mic_head")

        # 5. Integrated Central Pilot Swivel Chair
        if config.chair_included:
            chair_y = -d * 0.15
            chair_z = 0.46
            # Heavy floor pedestal column
            MeshBuilder.add_cylinder(bm, (0, chair_y, chair_z / 2), 0.06, chair_z, sides=6, mat_idx=m_body, name="chair_pedestal")
            MeshBuilder.add_cylinder(bm, (0, chair_y, 0.02), 0.22, 0.04, sides=8, mat_idx=m_steel, name="chair_floor_flange")

            # Thick vinyl seat cushion
            MeshBuilder.add_box(bm, (0, chair_y, chair_z + 0.04), (0.52, 0.48, 0.08), m_chair, "pilot_seat")

            # High backrest with headrest
            back_h = 0.65
            MeshBuilder.add_box(bm, (0, chair_y - 0.22, chair_z + 0.08 + back_h / 2), (0.46, 0.08, back_h), m_chair, "pilot_backrest")
            MeshBuilder.add_box(bm, (0, chair_y - 0.22, chair_z + 0.08 + back_h + 0.05), (0.34, 0.09, 0.14), m_chair, "pilot_headrest")

            # Padded armrests
            for ax in (-0.28, 0.28):
                MeshBuilder.add_box(bm, (ax, chair_y, chair_z + 0.20), (0.07, 0.34, 0.04), m_chair, "pilot_armrest")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
