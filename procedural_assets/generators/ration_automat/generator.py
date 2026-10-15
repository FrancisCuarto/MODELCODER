import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import RationAutomatConfig

class RationAutomatGenerator(BaseGenerator):
    """Generates heavy brutalist food ration automats and synthetic cigarette vending machines."""

    def generate(self, config: RationAutomatConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        h = config.height
        d = config.depth

        m_casing = mat_mgr.get_material_index("casing")
        m_front = mat_mgr.get_material_index("locker_gray")
        m_steel = mat_mgr.get_material_index("mounting")
        m_window = mat_mgr.get_material_index("crt_screen_amber" if config.display_color == "amber" else "crt_screen_green")
        m_disp = mat_mgr.get_material_index("casing_inner")
        m_prod = mat_mgr.get_material_index("chem_yellow" if "chem_yellow" in mat_mgr.palette else "button_yellow")
        m_btn = mat_mgr.get_material_index("button_gray")

        # 1. Main outer heavy housing cabinet
        base_h = 0.12
        body_h = h - base_h
        body_z = base_h + body_h / 2

        # Recessed dark kickplate base
        MeshBuilder.add_box(bm, (0, 0, base_h / 2), (w - 0.06, d - 0.06, base_h), m_casing, "base_recess")
        # Main upper body
        MeshBuilder.add_box(bm, (0, 0, body_z), (w, d, body_h), m_casing, "main_body")
        # Front face panel
        face_th = 0.04
        face_y = d / 2 + face_th / 2
        MeshBuilder.add_box(bm, (0, face_y - 0.01, body_z), (w - 0.04, face_th, body_h - 0.04), m_front, "front_face")

        # 2. Illuminated Product Showcase Window (Upper Half)
        win_w = w * 0.62
        win_h = body_h * 0.44
        win_z = h - win_h / 2 - 0.15
        win_x = -w * 0.12

        MeshBuilder.add_box(bm, (win_x, face_y + 0.01, win_z), (win_w, 0.03, win_h), m_steel, "window_frame")
        if config.dispenser_state != "smashed_glass":
            MeshBuilder.add_box(bm, (win_x, face_y + 0.02, win_z), (win_w - 0.06, 0.015, win_h - 0.06), m_window, "lit_display_screen")

        # Visible product shelves behind window
        shelf_rows = 3
        for r in range(shelf_rows):
            s_z = win_z - win_h / 2 + (r + 1) * (win_h / (shelf_rows + 1))
            MeshBuilder.add_box(bm, (win_x, face_y - 0.02, s_z), (win_w - 0.08, 0.08, 0.02), m_steel, f"shelf_{r}")
            # Low poly ration packets
            for px in (-0.14, 0.0, 0.14):
                MeshBuilder.add_box(bm, (win_x + px, face_y - 0.01, s_z + 0.045), (0.07, 0.06, 0.07), m_prod, "product_box")

        # 3. Side Control Column (Keypad, Credit Reader, Return Lever)
        ctrl_x = w / 2 - (w * 0.18)
        ctrl_y = face_y + 0.015

        # Keypad panel
        if config.has_keypad:
            MeshBuilder.add_box(bm, (ctrl_x, ctrl_y, win_z + 0.08), (0.16, 0.03, 0.22), m_steel, "keypad_bezel")
            # 3x4 small numeric buttons
            for bx in (-0.04, 0.0, 0.04):
                for bz in (-0.06, -0.02, 0.02, 0.06):
                    MeshBuilder.add_box(bm, (ctrl_x + bx, ctrl_y + 0.02, win_z + 0.08 + bz), (0.025, 0.015, 0.025), m_btn, "key_btn")

        # Coin / Card Chit Slot
        if config.has_coin_card_slot:
            MeshBuilder.add_box(bm, (ctrl_x, ctrl_y, win_z - 0.12), (0.14, 0.025, 0.07), m_steel, "card_slot_housing")
            MeshBuilder.add_box(bm, (ctrl_x, ctrl_y + 0.015, win_z - 0.12), (0.08, 0.01, 0.01), m_casing, "card_slot_slit")

        # 4. Bottom Dispensing Delivery Bin Flap
        bin_w = w * 0.72
        bin_h = 0.28
        bin_z = base_h + bin_h / 2 + 0.08

        # Recessed bin frame
        MeshBuilder.add_box(bm, (0, face_y + 0.005, bin_z), (bin_w, 0.05, bin_h), m_steel, "bin_frame")

        if config.dispenser_state == "jammed_door":
            # Flap tilted half inward
            MeshBuilder.add_box(bm, (0, face_y - 0.03, bin_z + 0.04), (bin_w - 0.04, 0.08, 0.02), m_disp, "jammed_flap")
            # Stuck ration cylinder / carton protruding
            MeshBuilder.add_box(bm, (0.05, face_y + 0.03, bin_z), (0.12, 0.18, 0.09), m_prod, "stuck_ration")
        else:
            # Closed flap
            MeshBuilder.add_box(bm, (0, face_y + 0.015, bin_z), (bin_w - 0.04, 0.02, bin_h - 0.04), m_disp, "bin_flap")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
