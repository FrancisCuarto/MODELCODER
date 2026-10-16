import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CableTrayConfig

class CableTrayGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial overhead cable ladder trays.
    Constructs galvanized C-channel stringers, slotted ladder rungs, suspension drop rods,
    bundled heavy electrical/telecom cables, and optional perforated top covers.
    """

    def generate(self, config: CableTrayConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CableTrayConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        l = self.config.tray_length
        w = self.config.tray_width
        h = self.config.tray_height
        half_l = l * 0.5
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        rubber_rgba = (0.12, 0.13, 0.14, 1.0)
        power_cable_rgba = (0.80, 0.35, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Longitudinal Side Rails (C-channel stringers)
        # -------------------------------------------------------------
        rail_th = 0.025
        for sx in (-half_w + rail_th * 0.5, half_w - rail_th * 0.5):
            MeshBuilder.add_box(
                bm,
                size=(rail_th, l, h),
                offset=(sx, 0.0, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Top stiffening lip
            MeshBuilder.add_box(
                bm,
                size=(rail_th * 1.5, l, 0.015),
                offset=(sx, 0.0, h * 0.5 - 0.0075),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 2. Transverse Cross Rungs (Ladder bottom supports)
        # -------------------------------------------------------------
        rung_spacing = max(0.20, self.config.rung_spacing)
        rung_count = max(3, int(l / rung_spacing))
        actual_step = l / (rung_count + 1)
        inner_w = w - rail_th * 2

        for i in range(1, rung_count + 1):
            ry = -half_l + i * actual_step
            MeshBuilder.add_box(
                bm,
                size=(inner_w, 0.035, 0.018),
                offset=(0.0, ry, -h * 0.5 + 0.009),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 3. Bundled Cables Resting on Rungs
        # -------------------------------------------------------------
        if self.config.cable_density > 0.05:
            # 3 main longitudinal cable bundles
            bundle_radii = [0.035, 0.028, 0.032, 0.022]
            bundle_xs = [-inner_w * 0.30, -inner_w * 0.05, inner_w * 0.22, inner_w * 0.38]
            bundle_mats = [rubber_rgba, power_cable_rgba, rubber_rgba, (0.2, 0.55, 0.85, 1.0)]

            num_cables = min(len(bundle_xs), max(1, int(len(bundle_xs) * self.config.cable_density * 1.2)))
            for ci in range(num_cables):
                bx = bundle_xs[ci]
                br = bundle_radii[ci]
                b_rgba = bundle_mats[ci]
                bz = -h * 0.5 + 0.018 + br

                MeshBuilder.add_cylinder(
                    bm,
                    radius=br,
                    depth=l * 0.98,
                    segments=5,
                    offset=(bx, 0.0, bz),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=b_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

                # Plastic zip-ties / cable cleats along length
                for ti in range(1, rung_count + 1, 2):
                    ty = -half_l + ti * actual_step
                    MeshBuilder.add_box(
                        bm,
                        size=(br * 2.4, 0.015, 0.01),
                        offset=(bx, ty, bz + br),
                        mat_idx=accent_mat,
                        rgba=(0.95, 0.85, 0.2, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                    )

        # -------------------------------------------------------------
        # 4. Sagging / Dangling Loose Wires (Optional)
        # -------------------------------------------------------------
        if self.config.has_hanging_cables:
            # Droop loop extending down on one side
            wire_r = 0.012
            wire_x = half_w - 0.02
            MeshBuilder.add_cylinder(
                bm,
                radius=wire_r,
                depth=0.25,
                segments=4,
                offset=(wire_x + 0.03, 0.0, -h * 0.5 - 0.10),
                axis='Z',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )
            MeshBuilder.add_cylinder(
                bm,
                radius=wire_r,
                depth=0.18,
                segments=4,
                offset=(wire_x + 0.03, 0.08, -h * 0.5 - 0.16),
                axis='Y',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        # -------------------------------------------------------------
        # 5. Top Perforated Dust Cover (Optional)
        # -------------------------------------------------------------
        if self.config.has_cover:
            cover_th = 0.012
            MeshBuilder.add_box(
                bm,
                size=(w + 0.02, l, cover_th),
                offset=(0.0, 0.0, h * 0.5 + cover_th * 0.5),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # -------------------------------------------------------------
        # 6. Suspension Drop Rods & Beam Clamps (Optional)
        # -------------------------------------------------------------
        if self.config.has_suspension_rods:
            rod_r = 0.012
            rod_h = 0.60
            for sy in (-half_l + 0.25, half_l - 0.25):
                # Cross trapeze channel under the tray
                MeshBuilder.add_box(
                    bm,
                    size=(w + 0.10, 0.045, 0.03),
                    offset=(0.0, sy, -h * 0.5 - 0.015),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Vertical threaded rods on left and right
                for rx in (-(w + 0.08) * 0.5, (w + 0.08) * 0.5):
                    # Vertical rod
                    MeshBuilder.add_box(
                        bm,
                        size=(rod_r * 2, rod_r * 2, rod_h),
                        offset=(rx, sy, -h * 0.5 + rod_h * 0.5),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                    )
                    # Ceiling unistrut bracket / flange
                    MeshBuilder.add_box(
                        bm,
                        size=(0.06, 0.06, 0.02),
                        offset=(rx, sy, -h * 0.5 + rod_h),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
