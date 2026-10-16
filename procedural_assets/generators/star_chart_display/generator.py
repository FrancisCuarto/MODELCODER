import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import StarChartDisplayConfig

class StarChartDisplayGenerator(BaseAssetGenerator):
    """
    Procedural generator for large-format wall-mounted star chart and orbital navigation displays.
    Builds perimeter reinforced bezel frame, corner anchor gussets, backlit tactical CRT screen,
    overhead illumination cowl, and lower layer-selection button strip.
    """

    def generate(self, config: StarChartDisplayConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = StarChartDisplayConfig()

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

        mode_colors = {
            "orbital_plot": (0.18, 0.65, 0.55, 1.0),
            "star_map": (0.12, 0.45, 0.68, 1.0),
            "alert_route": (0.95, 0.20, 0.15, 1.0),
            "dark_offline": (0.10, 0.12, 0.14, 1.0)
        }
        screen_rgba = mode_colors.get(self.config.display_mode, mode_colors["orbital_plot"])

        w = max(0.8, self.config.width)
        h = max(0.5, self.config.height)
        d = max(0.05, self.config.depth)
        half_w = w * 0.5
        half_h = h * 0.5

        # -------------------------------------------------------------
        # 1. Main Wall Mount Backplate & Bezel Frame
        # -------------------------------------------------------------
        # Rear structural box against wall Y=0
        MeshBuilder.add_box(
            bm,
            size=(w, d, h),
            offset=(0.0, d * 0.5, 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        front_y = d

        # Raised perimeter bezel border
        frame_t = 0.04
        # Top & Bottom frame bars
        for fz in (-half_h + (frame_t * 0.5), half_h - (frame_t * 0.5)):
            MeshBuilder.add_box(
                bm,
                size=(w, 0.015, frame_t),
                offset=(0.0, front_y + 0.0075, fz),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        # Left & Right frame bars
        for fx in (-half_w + (frame_t * 0.5), half_w - (frame_t * 0.5)):
            MeshBuilder.add_box(
                bm,
                size=(frame_t, 0.015, h - (frame_t * 2.0)),
                offset=(fx, front_y + 0.0075, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 2. Inset Emissive Star Chart / Orbital Screen
        # -------------------------------------------------------------
        screen_w = w - (frame_t * 2.0) - 0.02
        screen_h = h - (frame_t * 2.0) - 0.08  # Reserve space for lower buttons
        screen_z = 0.035
        MeshBuilder.add_box(
            bm,
            size=(screen_w, 0.008, screen_h),
            offset=(0.0, front_y + 0.004, screen_z),
            mat_idx=accent_mat,
            rgba=screen_rgba,
            uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
        )

        # -------------------------------------------------------------
        # 3. Corner Reinforcement Gusset Brackets
        # -------------------------------------------------------------
        if self.config.has_corner_brackets:
            gusset_size = 0.07
            for cx in (-half_w + (gusset_size * 0.5), half_w - (gusset_size * 0.5)):
                for cz in (-half_h + (gusset_size * 0.5), half_h - (gusset_size * 0.5)):
                    MeshBuilder.add_box(
                        bm,
                        size=(gusset_size, 0.022, gusset_size),
                        offset=(cx, front_y + 0.011, cz),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                    )

        # -------------------------------------------------------------
        # 4. Lower Layer-Selection Control Strip
        # -------------------------------------------------------------
        if self.config.has_control_strip:
            strip_z = -half_h + frame_t + 0.03
            # Background strip panel
            MeshBuilder.add_box(
                bm,
                size=(screen_w, 0.008, 0.045),
                offset=(0.0, front_y + 0.006, strip_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Array of 6 tactical selector buttons
            btn_count = 6
            btn_step = (screen_w * 0.75) / (btn_count - 1)
            btn_start_x = -(screen_w * 0.75) * 0.5
            for bi in range(btn_count):
                bx = btn_start_x + (bi * btn_step)
                MeshBuilder.add_box(
                    bm,
                    size=(0.035, 0.012, 0.025),
                    offset=(bx, front_y + 0.012, strip_z),
                    mat_idx=casing_mat,
                    rgba=(0.32, 0.35, 0.38, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
                )

        # -------------------------------------------------------------
        # 5. Top Overhead Illumination Hood Brow
        # -------------------------------------------------------------
        hood_d = 0.08
        MeshBuilder.add_box(
            bm,
            size=(w + 0.04, hood_d, 0.035),
            offset=(0.0, (hood_d * 0.5) - 0.01, half_h + 0.015),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
