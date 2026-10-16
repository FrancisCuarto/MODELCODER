import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import MicroscopeConfig

class MicroscopeGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for clinical laboratory optical microscopes.
    Features heavy horseshoe base, sub-stage halogen illuminator, mechanical stage
    with slide clips, rotating objective nosepiece, focus knobs, and inclined binocular head.
    """

    def generate(self, config: MicroscopeConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = MicroscopeConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        h = self.config.total_height
        scale = h / 0.48

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)
        lens_rgba = (0.9, 0.95, 1.0, 1.0) if self.config.is_illuminator_on else (0.4, 0.5, 0.55, 0.8)

        # -------------------------------------------------------------
        # 1. Cast Horseshoe Base & Feet
        # -------------------------------------------------------------
        base_w = 0.22 * scale
        base_l = 0.28 * scale
        base_h = 0.05 * scale

        MeshBuilder.add_box(
            bm,
            size=(base_w, base_l, base_h),
            offset=(0.0, 0.02 * scale, base_h * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Rubber support feet (4 pads)
        foot_r = 0.025 * scale
        foot_h = 0.015 * scale
        for fx in (-base_w * 0.4, base_w * 0.4):
            for fy in (-base_l * 0.38 + 0.02 * scale, base_l * 0.38 + 0.02 * scale):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=foot_r,
                    depth=foot_h,
                    segments=6,
                    offset=(fx, fy, foot_h * 0.5),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # Sub-stage light source housing
        lamp_r = 0.04 * scale
        lamp_h = 0.035 * scale
        lamp_pos = (0.0, -0.04 * scale, base_h + lamp_h * 0.5)
        MeshBuilder.add_cylinder(
            bm,
            radius=lamp_r,
            depth=lamp_h,
            segments=6,
            offset=lamp_pos,
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Illuminator lens
        lens_uv = "fluorescent_lit" if self.config.is_illuminator_on else "glass_reinforced"
        MeshBuilder.add_cylinder(
            bm,
            radius=lamp_r * 0.75,
            depth=0.01 * scale,
            segments=6,
            offset=(0.0, -0.04 * scale, base_h + lamp_h),
            axis='Z',
            mat_idx=screen_mat,
            rgba=lens_rgba,
            uv_rect=PS1TextureAtlas.get_rect(lens_uv)
        )

        # -------------------------------------------------------------
        # 2. Upright Curved Arm & Focus Adjustment Knobs
        # -------------------------------------------------------------
        arm_w = 0.07 * scale
        arm_d = 0.08 * scale
        arm_h = 0.30 * scale
        arm_y = 0.08 * scale
        arm_z = base_h + arm_h * 0.5

        # Vertical pillar
        MeshBuilder.add_box(
            bm,
            size=(arm_w, arm_d, arm_h),
            offset=(0.0, arm_y, arm_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Upper neck forward over stage
        neck_len = 0.14 * scale
        MeshBuilder.add_box(
            bm,
            size=(arm_w, neck_len, 0.06 * scale),
            offset=(0.0, arm_y - neck_len * 0.35, base_h + arm_h - 0.03 * scale),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Focus Adjustment Knobs
        knob_z = base_h + 0.12 * scale
        for side in (-1.0, 1.0):
            # Coarse focus wheel
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035 * scale,
                depth=0.025 * scale,
                segments=6,
                offset=(side * (arm_w * 0.5 + 0.02 * scale), arm_y, knob_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )
            # Fine focus wheel
            MeshBuilder.add_cylinder(
                bm,
                radius=0.020 * scale,
                depth=0.020 * scale,
                segments=6,
                offset=(side * (arm_w * 0.5 + 0.04 * scale), arm_y, knob_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 3. Mechanical Stage & Slide
        # -------------------------------------------------------------
        stage_z = base_h + 0.14 * scale + (self.config.stage_elevation - 0.5) * 0.04 * scale
        stage_w = 0.16 * scale
        stage_d = 0.15 * scale
        stage_th = 0.015 * scale

        MeshBuilder.add_box(
            bm,
            size=(stage_w, stage_d, stage_th),
            offset=(0.0, -0.02 * scale, stage_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Stage support bracket
        MeshBuilder.add_box(
            bm,
            size=(0.05 * scale, arm_y - (-0.02 * scale), 0.05 * scale),
            offset=(0.0, (arm_y - 0.02 * scale) * 0.5, stage_z - 0.03 * scale),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Glass specimen slide
        if self.config.has_slide_on_stage:
            MeshBuilder.add_box(
                bm,
                size=(0.09 * scale, 0.04 * scale, 0.005 * scale),
                offset=(0.0, -0.03 * scale, stage_z + stage_th * 0.5 + 0.003 * scale),
                mat_idx=glass_mat,
                rgba=(0.5, 0.7, 0.8, 0.7),
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )
            # Specimen cover slip smear
            MeshBuilder.add_box(
                bm,
                size=(0.03 * scale, 0.03 * scale, 0.002 * scale),
                offset=(0.0, -0.03 * scale, stage_z + stage_th * 0.5 + 0.007 * scale),
                mat_idx=screen_mat,
                rgba=(0.8, 0.6, 0.2, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )
            # Stage clip
            MeshBuilder.add_box(
                bm,
                size=(0.015 * scale, 0.05 * scale, 0.005 * scale),
                offset=(-0.035 * scale, -0.01 * scale, stage_z + stage_th * 0.5 + 0.006 * scale),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 4. Revolving Nosepiece Turret & Objectives
        # -------------------------------------------------------------
        turret_pos = (0.0, -0.03 * scale, base_h + arm_h - 0.07 * scale)
        MeshBuilder.add_cylinder(
            bm,
            radius=0.055 * scale,
            depth=0.03 * scale,
            segments=6,
            offset=turret_pos,
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        obj_count = max(3, min(self.config.objective_count, 4))
        obj_lens_r = 0.014 * scale
        obj_lens_len = 0.055 * scale
        turret_ring_r = 0.035 * scale

        band_colors = [
            ("button_red", (0.85, 0.15, 0.15, 1.0)),
            ("button_yellow", (0.9, 0.85, 0.15, 1.0)),
            ("button_blue", (0.15, 0.45, 0.85, 1.0)),
            ("button_white", (0.9, 0.9, 0.9, 1.0))
        ]

        for i in range(obj_count):
            theta = (2.0 * math.pi * i) / obj_count
            ox = math.cos(theta) * turret_ring_r
            oy = math.sin(theta) * turret_ring_r

            lens_mid = (turret_pos[0] + ox, turret_pos[1] + oy, turret_pos[2] - obj_lens_len * 0.5)
            MeshBuilder.add_cylinder(
                bm,
                radius=obj_lens_r,
                depth=obj_lens_len,
                segments=6,
                offset=lens_mid,
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Color band
            band_uv, band_rgba = band_colors[i % len(band_colors)]
            MeshBuilder.add_cylinder(
                bm,
                radius=obj_lens_r * 1.08,
                depth=0.012 * scale,
                segments=6,
                offset=(lens_mid[0], lens_mid[1], lens_mid[2] + obj_lens_len * 0.2),
                axis='Z',
                mat_idx=metal_mat,
                rgba=band_rgba,
                uv_rect=PS1TextureAtlas.get_rect(band_uv)
            )

        # -------------------------------------------------------------
        # 5. Inclined Head & Eyepieces
        # -------------------------------------------------------------
        head_pos = (0.0, arm_y - 0.02 * scale, base_h + arm_h + 0.02 * scale)

        MeshBuilder.add_box(
            bm,
            size=(0.11 * scale, 0.10 * scale, 0.08 * scale),
            offset=head_pos,
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        is_binocular = (self.config.eyepiece_type == "binocular")
        ocular_offsets = [-0.032 * scale, 0.032 * scale] if is_binocular else [0.0]

        for oc_x in ocular_offsets:
            oc_tube_len = 0.08 * scale
            oc_pos = (head_pos[0] + oc_x, head_pos[1] - 0.04 * scale, head_pos[2] + 0.05 * scale)

            MeshBuilder.add_cylinder(
                bm,
                radius=0.018 * scale,
                depth=oc_tube_len,
                segments=6,
                offset=oc_pos,
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Eyecup
            MeshBuilder.add_cylinder(
                bm,
                radius=0.024 * scale,
                depth=0.02 * scale,
                segments=6,
                offset=(oc_pos[0], oc_pos[1], oc_pos[2] + oc_tube_len * 0.5),
                axis='Z',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
