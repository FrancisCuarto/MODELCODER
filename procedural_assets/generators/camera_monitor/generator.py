import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CameraMonitorConfig

class CameraMonitorGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial CRT surveillance monitors with multi-channel feeds.
    Builds beveled monitor chassis, convex CRT phosphor glass, quad 2x2 grid divider,
    channel selector buttons, rotary dials, and tilt swivel desk stand.
    """

    def generate(self, config: CameraMonitorConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CameraMonitorConfig()

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

        feed_colors = {
            "cctv_feed": (0.22, 0.52, 0.38, 1.0),
            "static_noise": (0.42, 0.44, 0.48, 1.0),
            "no_signal": (0.12, 0.16, 0.42, 1.0),
            "standby": (0.09, 0.09, 0.10, 1.0)
        }
        screen_rgba = feed_colors.get(self.config.display_state, feed_colors["cctv_feed"])

        w = 0.38
        h = 0.30
        d = 0.28
        half_w = w * 0.5
        half_h = h * 0.5

        # Vertical base offset depending on swivel stand
        stand_h = 0.08 if self.config.has_desk_swivel_stand else 0.015
        mon_z = stand_h + half_h

        # -------------------------------------------------------------
        # 1. Swivel Stand or Rubber Feet
        # -------------------------------------------------------------
        if self.config.has_desk_swivel_stand:
            # Circular base plate on desk
            MeshBuilder.add_cylinder(
                bm,
                radius=0.12,
                depth=0.018,
                segments=8,
                offset=(0.0, 0.0, 0.009),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Neck column
            MeshBuilder.add_cylinder(
                bm,
                radius=0.042,
                depth=stand_h - 0.018,
                segments=6,
                offset=(0.0, 0.0, 0.018 + ((stand_h - 0.018) * 0.5)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        else:
            # 4 rubber foot studs
            for fx in (-half_w * 0.75, half_w * 0.75):
                for fy in (-d * 0.35, d * 0.35):
                    MeshBuilder.add_box(
                        bm,
                        size=(0.03, 0.03, stand_h),
                        offset=(fx, fy, stand_h * 0.5),
                        mat_idx=metal_mat,
                        rgba=(0.12, 0.12, 0.14, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
                    )

        # -------------------------------------------------------------
        # 2. Main CRT Monitor Cabinet
        # -------------------------------------------------------------
        # Main housing body box
        MeshBuilder.add_box(
            bm,
            size=(w, d, h),
            offset=(0.0, 0.0, mon_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Rear vent louver box
        MeshBuilder.add_box(
            bm,
            size=(w * 0.75, 0.04, h * 0.65),
            offset=(0.0, -d * 0.5 - 0.02, mon_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_vent_grate")
        )
        # Top carrying handle recess
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.04, 0.018),
            offset=(0.0, 0.0, mon_z + half_h + 0.009),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        front_y = d * 0.5

        # -------------------------------------------------------------
        # 3. Front Screen Bezel & CRT Glass
        # -------------------------------------------------------------
        bezel_w = w * 0.88
        bezel_h = h * 0.68
        bezel_z = mon_z + 0.025

        # Raised outer frame surround
        MeshBuilder.add_box(
            bm,
            size=(bezel_w, 0.015, bezel_h),
            offset=(0.0, front_y + 0.0075, bezel_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Inset glowing CRT phosphor screen glass
        screen_w = bezel_w - 0.03
        screen_h = bezel_h - 0.03
        MeshBuilder.add_box(
            bm,
            size=(screen_w, 0.008, screen_h),
            offset=(0.0, front_y + 0.014, bezel_z),
            mat_idx=accent_mat,
            rgba=screen_rgba,
            uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
        )

        # Quad 2x2 grid cross splitter bars (if quad_split)
        if self.config.screen_layout == "quad_split":
            # Vertical line
            MeshBuilder.add_box(
                bm,
                size=(0.008, 0.006, screen_h),
                offset=(0.0, front_y + 0.017, bezel_z),
                mat_idx=metal_mat,
                rgba=(0.10, 0.10, 0.12, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Horizontal line
            MeshBuilder.add_box(
                bm,
                size=(screen_w, 0.006, 0.008),
                offset=(0.0, front_y + 0.017, bezel_z),
                mat_idx=metal_mat,
                rgba=(0.10, 0.10, 0.12, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Under-Screen Control Deck
        # -------------------------------------------------------------
        if self.config.has_control_deck:
            deck_z = mon_z - (half_h * 0.65)
            # 4 Channel select push buttons
            for ci in range(4):
                bx = -0.10 + (ci * 0.032)
                MeshBuilder.add_box(
                    bm,
                    size=(0.018, 0.012, 0.014),
                    offset=(bx, front_y + 0.006, deck_z),
                    mat_idx=metal_mat,
                    rgba=(0.30, 0.30, 0.34, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
                )
                # Small channel tally LED above button
                led_c = (0.20, 0.95, 0.25, 1.0) if self.config.display_state == "cctv_feed" else (0.20, 0.20, 0.22, 1.0)
                MeshBuilder.add_box(
                    bm,
                    size=(0.006, 0.006, 0.006),
                    offset=(bx, front_y + 0.005, deck_z + 0.016),
                    mat_idx=accent_mat,
                    rgba=led_c,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

            # Rotary Contrast / Brightness Dials
            for di, dx in enumerate((0.08, 0.12)):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.014,
                    depth=0.014,
                    segments=6,
                    offset=(dx, front_y + 0.007, deck_z),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
