import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import FloorGratingConfig

class FloorGratingGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial floor trench gratings.
    Builds cast recessed curb frames, bearing bar arrays, cross-tie rods,
    service trench cavities with sub-floor conduits, and propped-open inspection variants.
    """

    def generate(self, config: FloorGratingConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = FloorGratingConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        l = self.config.panel_length
        w = self.config.panel_width
        d = self.config.grate_depth
        half_l = l * 0.5
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        rust_rgba = (0.50, 0.28, 0.18, 1.0)
        pipe_rgba = (0.22, 0.45, 0.55, 1.0)

        # -------------------------------------------------------------
        # 1. Floor Curb Frame & Perimeter Warning Stripe
        # -------------------------------------------------------------
        curb_w = 0.05
        curb_h = d * 1.10

        if self.config.has_recessed_frame:
            # 4 border curbs surrounding the trench
            curb_uv = "hazard_stripes" if self.config.has_warning_stripe else "metal_dark_grime"
            curb_rgba = (0.95, 0.85, 0.2, 1.0) if self.config.has_warning_stripe else metal_rgba

            # North curb
            MeshBuilder.add_box(
                bm,
                size=(w + curb_w * 2, curb_w, curb_h),
                offset=(0.0, half_l + curb_w * 0.5, curb_h * 0.5),
                mat_idx=accent_mat if self.config.has_warning_stripe else metal_mat,
                rgba=curb_rgba,
                uv_rect=PS1TextureAtlas.get_rect(curb_uv)
            )
            # South curb
            MeshBuilder.add_box(
                bm,
                size=(w + curb_w * 2, curb_w, curb_h),
                offset=(0.0, -half_l - curb_w * 0.5, curb_h * 0.5),
                mat_idx=accent_mat if self.config.has_warning_stripe else metal_mat,
                rgba=curb_rgba,
                uv_rect=PS1TextureAtlas.get_rect(curb_uv)
            )
            # West curb
            MeshBuilder.add_box(
                bm,
                size=(curb_w, l, curb_h),
                offset=(-half_w - curb_w * 0.5, 0.0, curb_h * 0.5),
                mat_idx=accent_mat if self.config.has_warning_stripe else metal_mat,
                rgba=curb_rgba,
                uv_rect=PS1TextureAtlas.get_rect(curb_uv)
            )
            # East curb
            MeshBuilder.add_box(
                bm,
                size=(curb_w, l, curb_h),
                offset=(half_w + curb_w * 0.5, 0.0, curb_h * 0.5),
                mat_idx=accent_mat if self.config.has_warning_stripe else metal_mat,
                rgba=curb_rgba,
                uv_rect=PS1TextureAtlas.get_rect(curb_uv)
            )

        # -------------------------------------------------------------
        # 2. Sub-Floor Trench Cavity and Utilities
        # -------------------------------------------------------------
        trench_depth = 0.28
        # Concrete / steel trench lining bottom
        MeshBuilder.add_box(
            bm,
            size=(w, l, 0.02),
            offset=(0.0, 0.0, -trench_depth),
            mat_idx=metal_mat,
            rgba=(0.10, 0.11, 0.12, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Process pipe running inside trench
        MeshBuilder.add_cylinder(
            bm,
            radius=0.065,
            depth=l * 1.05,
            segments=6,
            offset=(0.0, 0.0, -trench_depth + 0.09),
            axis='Y',
            mat_idx=metal_mat,
            rgba=pipe_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Power conduit along side
        MeshBuilder.add_cylinder(
            bm,
            radius=0.035,
            depth=l * 1.05,
            segments=5,
            offset=(-half_w * 0.60, 0.0, -trench_depth + 0.05),
            axis='Y',
            mat_idx=metal_mat,
            rgba=(0.15, 0.15, 0.16, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # -------------------------------------------------------------
        # 3. Grating Panel Geometry (Flat or Propped Open)
        # -------------------------------------------------------------
        is_open = self.config.is_raised or (self.config.trench_state == "propped_open")
        tilt_angle = math.radians(35.0) if is_open else 0.0
        cos_t = math.cos(tilt_angle)
        sin_t = math.sin(tilt_angle)

        hinge_y = half_l - 0.02
        hinge_z = curb_h * 0.5

        def transform_point(local_x, local_y, local_z):
            if not is_open:
                return (local_x, local_y, local_z)
            # Rotate around hinge along X axis
            dy = local_y - hinge_y
            dz = local_z - hinge_z
            new_y = hinge_y + dy * cos_t - dz * sin_t
            new_z = hinge_z + dy * sin_t + dz * cos_t
            return (local_x, new_y, new_z)

        # Outer frame of the grating panel
        grate_w = w - 0.015
        grate_l = l - 0.015
        half_gw = grate_w * 0.5
        half_gl = grate_l * 0.5
        frame_th = 0.025

        # 4 perimeter frame bars of the panel
        # Front frame bar
        p1 = transform_point(0.0, -half_gl + frame_th * 0.5, d * 0.5)
        MeshBuilder.add_box(bm, size=(grate_w, frame_th, d), offset=p1, mat_idx=metal_mat, rgba=metal_rgba, uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime"))
        # Rear frame bar
        p2 = transform_point(0.0, half_gl - frame_th * 0.5, d * 0.5)
        MeshBuilder.add_box(bm, size=(grate_w, frame_th, d), offset=p2, mat_idx=metal_mat, rgba=metal_rgba, uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime"))
        # Left frame bar
        p3 = transform_point(-half_gw + frame_th * 0.5, 0.0, d * 0.5)
        MeshBuilder.add_box(bm, size=(frame_th, grate_l, d), offset=p3, mat_idx=metal_mat, rgba=metal_rgba, uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime"))
        # Right frame bar
        p4 = transform_point(half_gw - frame_th * 0.5, 0.0, d * 0.5)
        MeshBuilder.add_box(bm, size=(frame_th, grate_l, d), offset=p4, mat_idx=metal_mat, rgba=metal_rgba, uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime"))

        # Longitudinal bearing bars
        bars = max(4, min(self.config.bar_density, 12))
        inner_pw = grate_w - frame_th * 2
        bar_spacing = inner_pw / (bars + 1)
        bar_th = 0.014
        bar_h = d * 0.90

        for bi in range(1, bars + 1):
            bx = -half_gw + frame_th + bi * bar_spacing
            pt = transform_point(bx, 0.0, d * 0.5)
            MeshBuilder.add_box(
                bm,
                size=(bar_th, grate_l - frame_th * 2, bar_h),
                offset=pt,
                mat_idx=casing_mat,
                rgba=rust_rgba if self.config.trench_state == "corroded_bent" else metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # Transverse cross-tie rods
        tie_count = 3
        tie_spacing = (grate_l - frame_th * 2) / (tie_count + 1)
        for ti in range(1, tie_count + 1):
            ty = -half_gl + frame_th + ti * tie_spacing
            pt = transform_point(0.0, ty, d * 0.70)
            MeshBuilder.add_box(
                bm,
                size=(inner_pw, 0.012, 0.012),
                offset=pt,
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # Lifting finger notch / hook slot
        p_notch = transform_point(0.0, -half_gl + frame_th * 1.5, d * 0.5)
        MeshBuilder.add_box(
            bm,
            size=(0.08, 0.03, d * 0.5),
            offset=p_notch,
            mat_idx=metal_mat,
            rgba=(0.08, 0.08, 0.09, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Kickstand rod if propped open
        if is_open:
            MeshBuilder.add_box(
                bm,
                size=(0.02, 0.02, 0.45),
                offset=(-half_gw * 0.8, -half_gl * 0.2, 0.20),
                mat_idx=accent_mat,
                rgba=(0.85, 0.55, 0.20, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
