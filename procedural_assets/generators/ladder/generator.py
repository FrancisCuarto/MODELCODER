import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import LadderConfig

class LadderGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial vertical access ladders with safety cages.
    Builds steel stringers, anti-slip rungs, wall standoff brackets, top walkthrough egress handrails,
    and hoop safety cages for high elevation climb safety.
    """

    def generate(self, config: LadderConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = LadderConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        h = self.config.ladder_height
        w = self.config.ladder_width
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        yellow_rgba = (0.95, 0.85, 0.20, 1.0)

        # -------------------------------------------------------------
        # 1. Main Vertical Side Stringers
        # -------------------------------------------------------------
        stringer_w = 0.04
        stringer_d = 0.06
        for sx in (-half_w, half_w):
            MeshBuilder.add_box(
                bm,
                size=(stringer_w, stringer_d, h),
                offset=(sx, 0.0, h * 0.5),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # -------------------------------------------------------------
        # 2. Ladder Rungs
        # -------------------------------------------------------------
        spacing = max(0.25, self.config.rung_spacing)
        rung_count = max(4, int(h / spacing))
        inner_w = w - stringer_w

        for ri in range(1, rung_count):
            rz = ri * spacing
            if rz >= h - 0.15:
                break

            # Missing rung simulation
            if self.config.ladder_condition == "missing_rung" and ri == 4:
                # Broken stub brackets only
                for sx in (-half_w + 0.02, half_w - 0.02):
                    MeshBuilder.add_box(
                        bm,
                        size=(0.025, 0.03, 0.025),
                        offset=(sx, 0.0, rz),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
                continue

            # Full welded tubular rung
            MeshBuilder.add_cylinder(
                bm,
                radius=0.016,
                depth=inner_w,
                segments=5,
                offset=(0.0, 0.0, rz),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 3. Wall Standoff Brackets (Anchors extending backwards in -Y)
        # -------------------------------------------------------------
        standoff_count = max(2, min(self.config.standoff_bracket_count, 5))
        standoff_spacing = h / standoff_count
        standoff_depth = 0.20

        for si in range(1, standoff_count + 1):
            sz = (si - 0.5) * standoff_spacing
            for sx in (-half_w, half_w):
                # Horizontal standoff bar
                MeshBuilder.add_box(
                    bm,
                    size=(0.035, standoff_depth, 0.035),
                    offset=(sx, -standoff_depth * 0.5, sz),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Wall mounting flange plate
                MeshBuilder.add_box(
                    bm,
                    size=(0.08, 0.015, 0.08),
                    offset=(sx, -standoff_depth, sz),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 4. Top Walkthrough Egress Handrails (Optional)
        # -------------------------------------------------------------
        if self.config.has_walkthrough_top:
            flair_h = 0.85
            for sx, sign_x in ((-half_w, -1), (half_w, 1)):
                # Vertical extension
                MeshBuilder.add_box(
                    bm,
                    size=(stringer_w, stringer_d, flair_h),
                    offset=(sx + sign_x * 0.06, 0.0, h + flair_h * 0.5),
                    mat_idx=casing_mat,
                    rgba=casing_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )
                # Top return loop elbow
                MeshBuilder.add_box(
                    bm,
                    size=(0.12, stringer_d, stringer_w),
                    offset=(sx + sign_x * 0.06, 0.0, h + flair_h),
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

        # -------------------------------------------------------------
        # 5. Protective Safety Hoop Cage (Optional)
        # -------------------------------------------------------------
        if self.config.has_safety_cage:
            cage_start = max(1.2, min(self.config.cage_start_height, h - 0.8))
            cage_span = h - cage_start
            hoop_spacing = 0.65
            hoop_count = max(2, int(cage_span / hoop_spacing) + 1)

            cage_radius = w * 0.72
            cage_center_y = cage_radius * 0.85

            for hi in range(hoop_count):
                hz = cage_start + hi * hoop_spacing
                if hz > h + 0.05:
                    break

                # Semi-circular protective hoop (approximated by 3 straight segments)
                # Left diagonal forward strut
                MeshBuilder.add_box(
                    bm,
                    size=(0.03, cage_center_y, 0.025),
                    offset=(-half_w * 0.85, cage_center_y * 0.5, hz),
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                # Right diagonal forward strut
                MeshBuilder.add_box(
                    bm,
                    size=(0.03, cage_center_y, 0.025),
                    offset=(half_w * 0.85, cage_center_y * 0.5, hz),
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                # Front cross bar
                MeshBuilder.add_box(
                    bm,
                    size=(w * 1.15, 0.03, 0.025),
                    offset=(0.0, cage_center_y, hz),
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

            # Vertical longitudinal cage tie straps (left, center, right)
            strap_len = cage_span + 0.10
            strap_z = cage_start + strap_len * 0.5
            for st_x, st_y in ((-half_w * 0.85, cage_center_y), (0.0, cage_center_y + 0.01), (half_w * 0.85, cage_center_y)):
                MeshBuilder.add_box(
                    bm,
                    size=(0.02, 0.015, strap_len),
                    offset=(st_x, st_y, strap_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
