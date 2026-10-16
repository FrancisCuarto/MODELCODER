import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import QuarantineBedConfig

class QuarantineBedGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for clinical quarantine and isolation beds.
    Features heavy hospital frame, articulated mattress deck, restraint straps,
    collapsible safety rails, IV drip pole, and vital signs terminal.
    """

    def generate(self, config: QuarantineBedConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = QuarantineBedConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        uv_layer = MeshBuilder.get_or_create_uv_layer(bm)
        col_layer = MeshBuilder.get_or_create_color_layer(bm)

        length = self.config.bed_length
        width = self.config.bed_width
        height = self.config.bed_height
        half_l = length * 0.5
        half_w = width * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        accent_rgba = self.material_manager.get_rgba("accent")
        screen_rgba = (0.2, 0.85, 0.45, 1.0)
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        # -------------------------------------------------------------
        # 1. Lower Chassis & Wheels
        # -------------------------------------------------------------
        wheel_radius = 0.06
        wheel_width = 0.04
        leg_inset_x = half_w - 0.08
        leg_inset_y = half_l - 0.12
        leg_top_z = height * 0.45

        # 4 Caster legs
        for lx in (-leg_inset_x, leg_inset_x):
            for ly in (-leg_inset_y, leg_inset_y):
                # Wheel
                MeshBuilder.add_cylinder(
                    bm,
                    radius=wheel_radius,
                    depth=wheel_width,
                    segments=6,
                    offset=(lx, ly, wheel_radius),
                    axis='X',
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

                # Leg vertical strut
                leg_h = leg_top_z - (wheel_radius * 1.5)
                MeshBuilder.add_box(
                    bm,
                    size=(0.05, 0.05, leg_h),
                    offset=(lx, ly, wheel_radius * 1.5 + leg_h * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # Lower Equipment Shelf / Tray
        tray_w = width - 0.22
        tray_l = length - 0.32
        MeshBuilder.add_box(
            bm,
            size=(tray_w, tray_l, 0.02),
            offset=(0.0, 0.0, leg_top_z * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Frame longitudinal tubes
        tube_th = 0.04
        deck_frame_z = height * 0.55
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(tube_th, length - 0.1, tube_th),
                offset=(sx * (half_w - 0.04), 0.0, deck_frame_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # -------------------------------------------------------------
        # 2. Headboard & Footboard
        # -------------------------------------------------------------
        # Headboard (+Y)
        hb_h = height * 0.55
        hb_z = deck_frame_z + hb_h * 0.5
        MeshBuilder.add_box(
            bm,
            size=(width - 0.06, 0.04, hb_h),
            offset=(0.0, half_l - 0.03, hb_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Headboard push bar
        MeshBuilder.add_box(
            bm,
            size=(width - 0.16, 0.03, 0.03),
            offset=(0.0, half_l + 0.01, deck_frame_z + hb_h),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Footboard (-Y)
        fb_h = height * 0.35
        fb_z = deck_frame_z + fb_h * 0.5
        MeshBuilder.add_box(
            bm,
            size=(width - 0.06, 0.04, fb_h),
            offset=(0.0, -half_l + 0.03, fb_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Chart clipboard
        MeshBuilder.add_box(
            bm,
            size=(0.24, 0.015, 0.28),
            offset=(0.0, -half_l + 0.005, fb_z + 0.05),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Mattress Deck & Foam Mattress
        # -------------------------------------------------------------
        mat_th = 0.12
        mat_w = width - 0.12
        mat_z = deck_frame_z + tube_th * 0.5 + mat_th * 0.5

        head_ratio = 0.35
        body_len = (length - 0.12) * (1.0 - head_ratio)
        head_len = (length - 0.12) * head_ratio

        # Main flat body section
        body_center_y = -half_l + 0.06 + body_len * 0.5
        MeshBuilder.add_box(
            bm,
            size=(mat_w, body_len, mat_th),
            offset=(0.0, body_center_y, mat_z),
            mat_idx=accent_mat,
            rgba=accent_rgba,
            uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
        )

        # Headrest section
        head_z_boost = math.sin(math.radians(max(0.0, min(self.config.headrest_angle, 45.0)))) * 0.15
        head_center_y = body_center_y + body_len * 0.5 + head_len * 0.5
        MeshBuilder.add_box(
            bm,
            size=(mat_w, head_len, mat_th),
            offset=(0.0, head_center_y, mat_z + head_z_boost * 0.5),
            mat_idx=accent_mat,
            rgba=accent_rgba,
            uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
        )

        # Pillow
        MeshBuilder.add_box(
            bm,
            size=(mat_w - 0.15, 0.28, 0.06),
            offset=(0.0, head_center_y + head_len * 0.25, mat_z + mat_th * 0.5 + 0.03 + head_z_boost),
            mat_idx=casing_mat,
            rgba=(0.90, 0.92, 0.94, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
        )

        # Patient covered bulk
        if self.config.has_patient_bulk:
            MeshBuilder.add_box(
                bm,
                size=(mat_w * 0.65, body_len * 0.75, 0.22),
                offset=(0.0, body_center_y, mat_z + mat_th * 0.5 + 0.11),
                mat_idx=casing_mat,
                rgba=(0.88, 0.90, 0.92, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
            )

        # -------------------------------------------------------------
        # 4. Restraint Containment Straps
        # -------------------------------------------------------------
        if self.config.has_restraint_straps:
            strap_ys = [body_center_y - body_len * 0.25, body_center_y + body_len * 0.15]
            for sy in strap_ys:
                sz = mat_z + mat_th * 0.5 + (0.22 if self.config.has_patient_bulk else 0.01)
                MeshBuilder.add_box(
                    bm,
                    size=(mat_w + 0.02, 0.06, 0.015),
                    offset=(0.0, sy, sz),
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )
                MeshBuilder.add_box(
                    bm,
                    size=(0.09, 0.08, 0.02),
                    offset=(0.0, sy, sz + 0.01),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 5. Safety Containment Rails
        # -------------------------------------------------------------
        rail_z_offset = 0.24 if self.config.rails_raised else -0.12
        rail_base_z = deck_frame_z + tube_th * 0.5 + rail_z_offset
        rail_len = length * 0.55
        rail_h = 0.28

        for side in (-1.0, 1.0):
            rx = side * (half_w - 0.02)
            # Top rail bar
            MeshBuilder.add_box(
                bm,
                size=(0.02, rail_len, 0.025),
                offset=(rx, -0.05, rail_base_z + rail_h),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Bottom rail bar
            MeshBuilder.add_box(
                bm,
                size=(0.02, rail_len, 0.02),
                offset=(rx, -0.05, rail_base_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # 3 Vertical rungs
            for rung_i in range(3):
                rung_y = -0.05 - rail_len * 0.4 + rung_i * (rail_len * 0.4)
                MeshBuilder.add_box(
                    bm,
                    size=(0.018, 0.018, rail_h),
                    offset=(rx, rung_y, rail_base_z + rail_h * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 6. IV Drip Pole
        # -------------------------------------------------------------
        if self.config.has_iv_pole:
            pole_x = -half_w + 0.05
            pole_y = half_l - 0.12
            pole_h = 1.35
            pole_z = deck_frame_z + pole_h * 0.5

            MeshBuilder.add_box(
                bm,
                size=(0.025, 0.025, pole_h),
                offset=(pole_x, pole_y, pole_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # T-hanger
            MeshBuilder.add_box(
                bm,
                size=(0.22, 0.02, 0.02),
                offset=(pole_x, pole_y, deck_frame_z + pole_h),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # IV Bag
            MeshBuilder.add_box(
                bm,
                size=(0.06, 0.03, 0.15),
                offset=(pole_x + 0.08, pole_y, deck_frame_z + pole_h - 0.12),
                mat_idx=casing_mat,
                rgba=(0.7, 0.85, 0.9, 0.8),
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )

        # -------------------------------------------------------------
        # 7. Articulated Vitals Monitor Arm
        # -------------------------------------------------------------
        if self.config.has_monitor_arm:
            arm_x = half_w - 0.04
            arm_y = half_l - 0.16
            arm_base_z = deck_frame_z + 0.25

            # Post
            MeshBuilder.add_box(
                bm,
                size=(0.03, 0.03, 0.5),
                offset=(arm_x, arm_y, arm_base_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Monitor chassis
            mon_x = arm_x + 0.05
            mon_y = arm_y - 0.15
            mon_z = arm_base_z + 0.32
            MeshBuilder.add_box(
                bm,
                size=(0.20, 0.12, 0.18),
                offset=(mon_x, mon_y, mon_z),
                mat_idx=casing_mat,
                rgba=(0.78, 0.76, 0.72, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )

            # Screen
            MeshBuilder.add_box(
                bm,
                size=(0.015, 0.09, 0.13),
                offset=(mon_x - 0.09, mon_y, mon_z),
                mat_idx=screen_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )

            # LED
            MeshBuilder.add_box(
                bm,
                size=(0.015, 0.02, 0.02),
                offset=(mon_x - 0.09, mon_y + 0.05, mon_z - 0.06),
                mat_idx=screen_mat,
                rgba=(0.1, 0.9, 0.2, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("led_green")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
