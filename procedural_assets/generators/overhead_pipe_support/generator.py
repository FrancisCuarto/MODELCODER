import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import OverheadPipeSupportConfig

class OverheadPipeSupportGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial overhead trapeze pipe supports.
    Builds structural beam clamps, threaded vertical drop rods, unistrut cross-channels,
    U-bolt pipe clamps, and through-running process conduits with industrial markings.
    """

    def generate(self, config: OverheadPipeSupportConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = OverheadPipeSupportConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.hanger_width
        dh = self.config.drop_height
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        coolant_rgba = (0.15, 0.65, 0.75, 1.0)
        fuel_rgba = (0.85, 0.40, 0.15, 1.0)
        steam_rgba = (0.75, 0.75, 0.78, 1.0)

        # -------------------------------------------------------------
        # 1. Top I-Beam Flange Clamps & Ceiling Brackets
        # -------------------------------------------------------------
        if self.config.has_beam_clamps:
            for sx in (-half_w, half_w):
                # Flange jaw clamp body
                MeshBuilder.add_box(
                    bm,
                    size=(0.09, 0.08, 0.06),
                    offset=(sx, 0.0, dh * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Heavy square lock bolt
                MeshBuilder.add_box(
                    bm,
                    size=(0.035, 0.035, 0.04),
                    offset=(sx, 0.0, dh * 0.5 + 0.04),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 2. Vertical Threaded Suspension Drop Rods
        # -------------------------------------------------------------
        rod_r = 0.014
        for sx in (-half_w, half_w):
            # Hex nut at top
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.04, 0.025),
                offset=(sx, 0.0, dh * 0.5 - 0.03),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Long threaded drop rod
            MeshBuilder.add_box(
                bm,
                size=(rod_r * 2, rod_r * 2, dh),
                offset=(sx, 0.0, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Hex nut at bottom
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.04, 0.025),
                offset=(sx, 0.0, -dh * 0.5 + 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 3. Horizontal Unistrut Cross-Channel Tiers
        # -------------------------------------------------------------
        tiers = max(1, min(self.config.pipe_tier_count, 2))
        is_bent = (self.config.hanger_state == "bent_overload")

        for ti in range(tiers):
            tz = -dh * 0.5 + 0.04 + ti * 0.35
            # Main slotted channel
            channel_w = w + 0.12
            channel_d = 0.05
            channel_h = 0.045

            MeshBuilder.add_box(
                bm,
                size=(channel_w, channel_d, channel_h),
                offset=(0.0, 0.0, tz),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Plastic/rubber end caps on unistrut
            for ex in (-channel_w * 0.5 + 0.01, channel_w * 0.5 - 0.01):
                MeshBuilder.add_box(
                    bm,
                    size=(0.02, channel_d * 1.05, channel_h * 1.05),
                    offset=(ex, 0.0, tz),
                    mat_idx=accent_mat,
                    rgba=(0.95, 0.85, 0.2, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

            # ---------------------------------------------------------
            # 4. Pipe Clamps and Conduits on this Tier
            # ---------------------------------------------------------
            slots = max(1, min(self.config.pipe_slots, 4))
            slot_spacing = (w - 0.15) / (slots + 1)
            pipe_diameters = [0.12, 0.09, 0.14, 0.08]
            pipe_colors = [coolant_rgba, fuel_rgba, steam_rgba, coolant_rgba]

            for si in range(1, slots + 1):
                px = -half_w + 0.075 + si * slot_spacing
                p_dia = pipe_diameters[(si - 1) % len(pipe_diameters)]
                p_rad = p_dia * 0.5
                p_rgba = pipe_colors[(si - 1) % len(pipe_colors)]
                py_pipe = 0.0
                pz_pipe = tz + channel_h * 0.5 + p_rad

                # Clamp condition check
                clamp_missing = (self.config.hanger_state == "missing_clamp" and si == slots)

                # Clamp saddle base on channel
                MeshBuilder.add_box(
                    bm,
                    size=(p_dia * 1.15, 0.04, 0.018),
                    offset=(px, 0.0, tz + channel_h * 0.5 + 0.009),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

                if not clamp_missing:
                    # U-Bolt loop over the pipe
                    u_height = p_dia + 0.03
                    for ux in (px - p_rad - 0.012, px + p_rad + 0.012):
                        # Vertical legs of U-bolt
                        MeshBuilder.add_box(
                            bm,
                            size=(0.014, 0.014, u_height),
                            offset=(ux, 0.0, tz + channel_h * 0.5 + u_height * 0.5),
                            mat_idx=metal_mat,
                            rgba=metal_rgba,
                            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                        )
                    # Top cross bar of U-bolt
                    MeshBuilder.add_box(
                        bm,
                        size=(p_dia + 0.038, 0.02, 0.014),
                        offset=(px, 0.0, pz_pipe + p_rad + 0.01),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                    )

                # Process pipe running through support
                if self.config.has_pipes_included:
                    pipe_len = 1.40
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=p_rad,
                        depth=pipe_len,
                        segments=6,
                        offset=(px, py_pipe, pz_pipe),
                        axis='Y',
                        mat_idx=metal_mat,
                        rgba=p_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
                    # Pipe identification label bands
                    MeshBuilder.add_box(
                        bm,
                        size=(p_dia * 1.05, 0.04, p_dia * 1.05),
                        offset=(px, 0.25, pz_pipe),
                        mat_idx=accent_mat,
                        rgba=(0.95, 0.85, 0.2, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("caution_label")
                    )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
