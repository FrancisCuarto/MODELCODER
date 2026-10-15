import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import CanteenCounterConfig

class CanteenCounterGenerator(BaseGenerator):
    """Generates industrial cafeteria service counters with tray slides and roll-up shutters."""

    def generate(self, config: CanteenCounterConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_body = mat_mgr.get_material_index("locker_gray")
        m_frame = mat_mgr.get_material_index("casing")
        m_shutter = mat_mgr.get_material_index("vent")

        # 1. Base Counter Cabinet
        plinth_h = 0.08
        cab_h = h - plinth_h
        cab_z = plinth_h + cab_h / 2

        # Recessed dark plinth
        MeshBuilder.add_box(bm, (0, 0, plinth_h / 2), (w - 0.06, d - 0.06, plinth_h), m_frame, "plinth")
        # Main cabinet body
        MeshBuilder.add_box(bm, (0, 0, cab_z), (w, d, cab_h), m_body, "counter_cabinet")
        # Stainless steel service countertop
        top_th = 0.05
        top_z = h + top_th / 2
        MeshBuilder.add_box(bm, (0, 0, top_z), (w + 0.04, d + 0.04, top_th), m_steel, "counter_top")

        # 2. Inset Bain-Marie Steam Table Pans
        if config.has_steam_pans:
            pan_w = 0.32
            pan_d = 0.45
            pan_depth = 0.03
            pan_x_offsets = [-w * 0.30, 0.0, w * 0.30]
            for px in pan_x_offsets:
                # Recessed pan well
                MeshBuilder.add_box(bm, (px, -0.05, top_z + 0.01), (pan_w, pan_d, 0.02), m_frame, "steam_pan_well")
                # Handle bar on lid
                MeshBuilder.add_box(bm, (px, -0.05, top_z + 0.03), (0.12, 0.03, 0.015), m_steel, "pan_handle")

        # 3. Front Tubular Tray Slider Rails
        if config.has_tray_rails:
            rail_z = h - 0.08
            rail_y = (d / 2) + 0.16
            rail_len = w + 0.08
            tube_r = 0.018

            # 3 Parallel horizontal tubular rails
            for r_idx in range(3):
                ry = (d / 2) + 0.08 + (r_idx * 0.08)
                MeshBuilder.add_cylinder(bm, (0, ry, rail_z), tube_r, rail_len, sides=4, axis='X', mat_idx=m_steel, name=f"tray_rail_{r_idx}")

            # 3 Triangular cantilever support brackets
            for bx in (-w * 0.38, 0.0, w * 0.38):
                MeshBuilder.add_box(bm, (bx, (d / 2) + 0.14, rail_z - 0.04), (0.04, 0.24, 0.03), m_steel, "bracket_horiz")
                # Diagonal strut to cabinet
                MeshBuilder.add_box(bm, (bx, (d / 2) + 0.08, rail_z - 0.12), (0.04, 0.14, 0.03), m_steel, "bracket_diag")

        # 4. Overhead Service Hatch Bulkhead Frame & Slatted Roll-up Shutter
        if config.counter_type == "service_hatch":
            post_h = 1.30
            post_top_z = h + post_h
            # Left & Right heavy vertical channel posts
            for px in (-w / 2 - 0.02, w / 2 + 0.02):
                MeshBuilder.add_box(bm, (px, -d / 4, h + post_h / 2), (0.08, 0.08, post_h), m_frame, "hatch_post")

            # Header housing box for rolled-up shutter
            header_h = 0.35
            header_z = post_top_z - header_h / 2
            MeshBuilder.add_box(bm, (0, -d / 4, header_z), (w + 0.12, 0.18, header_h), m_frame, "shutter_header_box")

            # Shutter curtain (persiana metálica)
            shutter_total_h = post_h - header_h
            curtain_w = w
            if config.roll_up_shutter == "closed":
                curtain_h = shutter_total_h
                curtain_z = h + curtain_h / 2
                MeshBuilder.add_box(bm, (0, -d / 4, curtain_z), (curtain_w, 0.03, curtain_h), m_shutter, "shutter_curtain")
            elif config.roll_up_shutter == "half_open":
                curtain_h = shutter_total_h * 0.50
                curtain_z = post_top_z - header_h - curtain_h / 2
                MeshBuilder.add_box(bm, (0, -d / 4, curtain_z), (curtain_w, 0.03, curtain_h), m_shutter, "shutter_curtain")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
