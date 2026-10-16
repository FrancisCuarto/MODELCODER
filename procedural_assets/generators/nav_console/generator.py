import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import NavConsoleConfig

class NavConsoleGenerator(BaseAssetGenerator):
    """
    Procedural generator for orbital navigation and space telemetry bridge consoles.
    Builds ergonomic angled console chassis, multi-screen CRT cluster, flight attitude joystick,
    sliding throttle lever, mechanical command keypad, and footrest pedestal.
    """

    def generate(self, config: NavConsoleConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = NavConsoleConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")

        screen_colors = {
            "active": (0.18, 0.55, 0.45, 1.0),
            "signal_lost": (0.95, 0.45, 0.15, 1.0),
            "standby": (0.15, 0.25, 0.50, 1.0),
            "offline": (0.10, 0.10, 0.12, 1.0)
        }
        screen_rgba = screen_colors.get(self.config.console_state, screen_colors["active"])

        w = max(1.0, self.config.width)
        d = max(0.7, self.config.depth)
        h = max(0.9, self.config.height)
        desk_h = 0.72

        half_w = w * 0.5
        half_d = d * 0.5

        # -------------------------------------------------------------
        # 1. Base Pedestal Plinth & Side Panels
        # -------------------------------------------------------------
        # Heavy floor base box
        plinth_w = w * 0.94
        plinth_d = d * 0.85
        plinth_h = 0.10
        MeshBuilder.add_box(
            bm,
            size=(plinth_w, plinth_d, plinth_h),
            offset=(0.0, 0.0, plinth_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        # Left and right side cabinet pylons
        pylon_w = 0.18
        pylon_h = desk_h - plinth_h
        for px in (-half_w + (pylon_w * 0.5), half_w - (pylon_w * 0.5)):
            MeshBuilder.add_box(
                bm,
                size=(pylon_w, plinth_d, pylon_h),
                offset=(px, 0.0, plinth_h + (pylon_h * 0.5)),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # Tubular steel footrest rail connecting the side pylons
        if self.config.has_footrest:
            MeshBuilder.add_cylinder(
                bm,
                radius=0.018,
                depth=w - (pylon_w * 2.0),
                segments=6,
                offset=(0.0, -0.15, 0.18),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 2. Main Desktop Work Surface & Front Armrest
        # -------------------------------------------------------------
        table_d = d * 0.52
        table_y = -d * 0.22
        MeshBuilder.add_box(
            bm,
            size=(w, table_d, 0.04),
            offset=(0.0, table_y, desk_h),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )
        # Padded front wrist rest
        MeshBuilder.add_box(
            bm,
            size=(w * 0.96, 0.06, 0.025),
            offset=(0.0, table_y - (table_d * 0.5) + 0.03, desk_h + 0.02),
            mat_idx=metal_mat,
            rgba=(0.14, 0.14, 0.16, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
        )

        # -------------------------------------------------------------
        # 3. Slanted Display Hood & CRT Monitors
        # -------------------------------------------------------------
        hood_y = d * 0.20
        hood_d = d * 0.44
        hood_h = h - desk_h
        hood_z = desk_h + (hood_h * 0.5)

        # Slanted console upper enclosure box
        MeshBuilder.add_box(
            bm,
            size=(w, hood_d, hood_h),
            offset=(0.0, hood_y, hood_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Front display fascia holding CRT screens
        sc_count = max(1, min(4, self.config.screen_count))
        sc_w = (w * 0.88) / sc_count
        sc_h = hood_h * 0.68
        fascia_y = hood_y - (hood_d * 0.5) - 0.01

        for si in range(sc_count):
            sx = -half_w * 0.88 + (sc_w * 0.5) + (si * sc_w)
            # Screen bezel frame
            MeshBuilder.add_box(
                bm,
                size=(sc_w - 0.02, 0.015, sc_h),
                offset=(sx, fascia_y, hood_z + 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Inner phosphor CRT screen glass
            MeshBuilder.add_box(
                bm,
                size=(sc_w - 0.04, 0.01, sc_h - 0.03),
                offset=(sx, fascia_y - 0.005, hood_z + 0.02),
                mat_idx=accent_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
            )

        # -------------------------------------------------------------
        # 4. Flight Controls (HOTAS Joystick & Throttle Lever)
        # -------------------------------------------------------------
        ctrl_z = desk_h + 0.02
        if self.config.has_joystick:
            # Flight stick base pod on the right
            joy_x = half_w * 0.55
            joy_y = table_y + 0.04
            MeshBuilder.add_box(
                bm,
                size=(0.10, 0.12, 0.03),
                offset=(joy_x, joy_y, ctrl_z + 0.015),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Angled joystick shaft
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.14,
                segments=6,
                offset=(joy_x, joy_y, ctrl_z + 0.09),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Contoured ergonomic grip head
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.06, 0.06),
                offset=(joy_x, joy_y + 0.01, ctrl_z + 0.16),
                mat_idx=metal_mat,
                rgba=(0.12, 0.12, 0.14, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )

        if self.config.has_throttle:
            # Sliding throttle lever block on the left
            thr_x = -half_w * 0.55
            thr_y = table_y + 0.04
            MeshBuilder.add_box(
                bm,
                size=(0.12, 0.14, 0.03),
                offset=(thr_x, thr_y, ctrl_z + 0.015),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Dual throttle handle levers
            for tx in (-0.022, 0.022):
                MeshBuilder.add_box(
                    bm,
                    size=(0.02, 0.05, 0.08),
                    offset=(thr_x + tx, thr_y, ctrl_z + 0.06),
                    mat_idx=accent_mat,
                    rgba=(0.95, 0.85, 0.20, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

        # Center mechanical keypad
        center_w = w * 0.32
        MeshBuilder.add_box(
            bm,
            size=(center_w, 0.16, 0.02),
            offset=(0.0, table_y + 0.04, ctrl_z + 0.01),
            mat_idx=metal_mat,
            rgba=(0.28, 0.28, 0.32, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
