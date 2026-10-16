import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import WaterRecyclerConfig

class WaterRecyclerGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial life-support water reclamation and reverse-osmosis units.
    Builds equipment cabinet housing, multi-stage tubular filter vessels, stainless manifold pipes,
    TDS purity indicator monitor, pressure gauges, and bypass quarter-turn valves.
    """

    def generate(self, config: WaterRecyclerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = WaterRecyclerConfig()

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

        purity_colors = {
            "nominal": (0.18, 0.75, 0.85, 1.0),
            "filter_saturated": (0.95, 0.65, 0.15, 1.0),
            "emergency_bypass": (0.95, 0.20, 0.15, 1.0),
            "derelict": (0.12, 0.12, 0.14, 1.0)
        }
        purity_rgba = purity_colors.get(self.config.recycler_state, purity_colors["nominal"])

        w = max(0.7, self.config.width)
        d = max(0.5, self.config.depth)
        h = max(1.2, self.config.height)

        half_w = w * 0.5
        half_d = d * 0.5

        # -------------------------------------------------------------
        # 1. Base Skid & Cabinet Enclosure
        # -------------------------------------------------------------
        # Base plinth
        MeshBuilder.add_box(
            bm,
            size=(w, d, 0.08),
            offset=(0.0, 0.0, 0.04),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        # Upper rear cabinet housing box
        top_h = h - 0.08
        MeshBuilder.add_box(
            bm,
            size=(w, d, top_h),
            offset=(0.0, 0.0, 0.08 + (top_h * 0.5)),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Front central recessed niche for filter cartridges
        niche_w = w * 0.82
        niche_h = h * 0.52
        niche_z = 0.08 + (h * 0.32)
        MeshBuilder.add_box(
            bm,
            size=(niche_w, 0.12, niche_h),
            offset=(0.0, half_d - 0.04, niche_z),
            mat_idx=metal_mat,
            rgba=(0.14, 0.14, 0.16, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Multi-Stage Reverse-Osmosis Filter Canisters
        # -------------------------------------------------------------
        stage_count = max(2, min(4, self.config.filter_stage_count))
        canister_r = 0.065
        canister_h = niche_h * 0.82
        c_step = (niche_w - (canister_r * 2.0)) / max(1, stage_count - 1)
        c_start_x = -niche_w * 0.5 + canister_r

        for ci in range(stage_count):
            cx = c_start_x + (ci * c_step)
            # Main cylindrical vessel
            MeshBuilder.add_cylinder(
                bm,
                radius=canister_r,
                depth=canister_h,
                segments=7,
                offset=(cx, half_d + 0.02, niche_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.88, 0.90, 0.94, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Top & bottom clamp retaining rings
            for rz in (niche_z - (canister_h * 0.45), niche_z + (canister_h * 0.45)):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=canister_r * 1.15,
                    depth=0.025,
                    segments=7,
                    offset=(cx, half_d + 0.02, rz),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                )

        # Interconnecting stainless horizontal pipe manifold
        MeshBuilder.add_cylinder(
            bm,
            radius=0.015,
            depth=niche_w * 0.88,
            segments=6,
            offset=(0.0, half_d + 0.02, niche_z + (canister_h * 0.48)),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Upper Instrumentation Panel & TDS Monitor
        # -------------------------------------------------------------
        upper_panel_z = 0.08 + (h * 0.75)

        # TDS Purity display screen
        if self.config.has_purity_monitor:
            MeshBuilder.add_box(
                bm,
                size=(0.24, 0.015, 0.12),
                offset=(-0.14, half_d + 0.005, upper_panel_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            MeshBuilder.add_box(
                bm,
                size=(0.21, 0.010, 0.09),
                offset=(-0.14, half_d + 0.012, upper_panel_z),
                mat_idx=accent_mat,
                rgba=purity_rgba,
                uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
            )

        # Dual analog pressure gauges (Inlet & Outlet)
        for gi, gx in enumerate((0.14, 0.28)):
            MeshBuilder.add_cylinder(
                bm,
                radius=0.038,
                depth=0.02,
                segments=7,
                offset=(gx, half_d + 0.01, upper_panel_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.92, 0.92, 0.94, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
            )
            # Gauge needle
            MeshBuilder.add_box(
                bm,
                size=(0.006, 0.008, 0.03),
                offset=(gx, half_d + 0.022, upper_panel_z),
                mat_idx=accent_mat,
                rgba=(0.95, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # -------------------------------------------------------------
        # 4. Lower Bypass Quarter-Turn Ball Valves
        # -------------------------------------------------------------
        if self.config.has_bypass_valves:
            valve_z = 0.14
            for vi, vx in enumerate((-0.18, 0.18)):
                # Valve body
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.028,
                    depth=0.04,
                    segments=6,
                    offset=(vx, half_d + 0.02, valve_z),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Valve lever handle
                MeshBuilder.add_box(
                    bm,
                    size=(0.09, 0.018, 0.02),
                    offset=(vx + 0.03, half_d + 0.045, valve_z),
                    mat_idx=accent_mat,
                    rgba=(0.95, 0.85, 0.20, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
