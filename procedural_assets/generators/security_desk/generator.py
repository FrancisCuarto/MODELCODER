import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import SecurityDeskConfig

class SecurityDeskGenerator(BaseGenerator):
    """Generates security intake counters with bulletproof glass partitions, CCTV monitors, and intercorns."""

    def generate(self, config: SecurityDeskConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_armor = mat_mgr.get_material_index("casing")
        m_counter = mat_mgr.get_material_index("mounting")
        m_inner = mat_mgr.get_material_index("locker_gray")
        m_glass = mat_mgr.get_material_index("glass_tube")
        m_crt = mat_mgr.get_material_index("crt_screen_green")
        m_alert = mat_mgr.get_material_index("button_red")

        # 1. Armored Counter Pedestal
        plinth_h = 0.08
        cab_h = h - plinth_h
        cab_z = plinth_h + cab_h / 2

        # Front kickplate
        MeshBuilder.add_box(bm, (0, 0, plinth_h / 2), (w - 0.04, d - 0.04, plinth_h), m_armor, "plinth")

        # Armored front facade
        MeshBuilder.add_box(bm, (0, d / 2 - 0.03, cab_z), (w, 0.06, cab_h), m_armor, "front_armor_plate")
        # Side barrier wing
        MeshBuilder.add_box(bm, (-w / 2 + 0.03, 0, cab_z), (0.06, d, cab_h), m_armor, "side_wing_L")
        MeshBuilder.add_box(bm, (w / 2 - 0.03, 0, cab_z), (0.06, d, cab_h), m_armor, "side_wing_R")

        # Countertop with transaction pass-through dip
        top_th = 0.05
        top_z = h + top_th / 2
        MeshBuilder.add_box(bm, (0, 0, top_z), (w + 0.04, d + 0.04, top_th), m_counter, "countertop")

        # Recessed curved document pass-through tray
        MeshBuilder.add_box(bm, (0, d / 2 - 0.08, top_z + 0.01), (0.35, 0.22, 0.015), m_inner, "pass_through_tray")

        # 2. Bulletproof Polycarbonate / Glass Partition
        if config.bulletproof_glass:
            screen_h = 0.85
            screen_z = h + top_th + screen_h / 2
            front_y = d / 2 - 0.04

            # Upright steel support mullion posts
            for px in (-w / 2 + 0.04, 0.0, w / 2 - 0.04):
                MeshBuilder.add_box(bm, (px, front_y, screen_z), (0.05, 0.05, screen_h), m_armor, "mullion_post")

            # Top header cap bar
            MeshBuilder.add_box(bm, (0, front_y, h + top_th + screen_h), (w, 0.06, 0.04), m_armor, "header_cap")

            # Bulletproof glass panes
            if config.glass_damage != "smashed":
                pane_w = (w / 2) - 0.06
                for pane_x in (-w / 4, w / 4):
                    MeshBuilder.add_box(bm, (pane_x, front_y, screen_z - 0.02), (pane_w, 0.02, screen_h - 0.08), m_glass, "glass_pane")

            # Circular intercom speaker grille
            if config.has_intercom_grille:
                MeshBuilder.add_cylinder(bm, (0, front_y + 0.015, h + 0.40), 0.07, 0.02, sides=8, axis='Y', mat_idx=m_counter, name="intercom_grille")

        # 3. Arm-Mounted CCTV Surveillance CRT Monitor
        if config.has_cctv_monitor:
            mon_x = (w / 2) - 0.25
            mon_y = -d * 0.15
            mon_z = h + 0.42

            # Articulated support arm from desk
            MeshBuilder.add_cylinder(bm, (mon_x, mon_y, (h + mon_z) / 2), 0.02, mon_z - h, sides=4, mat_idx=m_counter, name="cctv_arm_post")
            # CRT monitor casing box
            mon_w, mon_h_size, mon_d = 0.32, 0.26, 0.30
            MeshBuilder.add_box(bm, (mon_x, mon_y + 0.08, mon_z), (mon_w, mon_d, mon_h_size), m_armor, "cctv_casing")
            # Glowing CRT phosphor face
            MeshBuilder.add_box(bm, (mon_x, mon_y - 0.06, mon_z), (mon_w - 0.04, 0.02, mon_h_size - 0.04), m_crt, "cctv_screen")

        # 4. Under-Counter Guard Shelf & Emergency Button
        if config.has_under_counter_shelf:
            shelf_z = h * 0.55
            shelf_w = w - 0.16
            shelf_d = d * 0.65
            MeshBuilder.add_box(bm, (0, -d * 0.10, shelf_z), (shelf_w, shelf_d, 0.03), m_inner, "under_shelf")

            # Red alarm push button under counter lip
            MeshBuilder.add_cylinder(bm, (0.25, -d * 0.25, h - 0.03), 0.03, 0.025, sides=6, mat_idx=m_alert, name="alarm_button")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
