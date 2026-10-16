import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SampleAnalyzerConfig

class SampleAnalyzerGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for automated laboratory sample spectrometers.
    Features angled benchtop chassis, motorized sample tray with vial vials,
    integrated CRT telemetry screen, status LEDs, barcode wand, and thermal printer.
    """

    def generate(self, config: SampleAnalyzerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = SampleAnalyzerConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.width
        d = self.config.depth
        h = self.config.height
        half_w = w * 0.5
        half_d = d * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        state = self.config.analyzer_state
        if state == "processing":
            screen_uv = "crt_screen_green"
            screen_rgba = (0.2, 0.85, 0.45, 1.0)
            led_active_uv = "led_yellow"
        elif state == "alarm" or state == "error":
            screen_uv = "crt_screen_amber"
            screen_rgba = (0.95, 0.45, 0.15, 1.0)
            led_active_uv = "led_red"
        else: # idle
            screen_uv = "crt_screen_off"
            screen_rgba = (0.15, 0.25, 0.20, 1.0)
            led_active_uv = "led_green"

        # -------------------------------------------------------------
        # 1. Base Housing & Rubber Dampeners
        # -------------------------------------------------------------
        base_h = 0.04
        MeshBuilder.add_box(
            bm,
            size=(w, d, base_h),
            offset=(0.0, 0.0, base_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        for fx in (-half_w * 0.8, half_w * 0.8):
            for fy in (-half_d * 0.8, half_d * 0.8):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.03,
                    depth=0.015,
                    segments=6,
                    offset=(fx, fy, 0.0075),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # -------------------------------------------------------------
        # 2. Main Enclosure (Chassis body)
        # -------------------------------------------------------------
        body_h = h - base_h
        body_z = base_h + body_h * 0.5
        MeshBuilder.add_box(
            bm,
            size=(w, d - 0.04, body_h),
            offset=(0.0, 0.02, body_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Angled front operator bezel
        bezel_w = w * 0.48
        bezel_h = body_h * 0.75
        bezel_x = -half_w * 0.42
        bezel_y = -half_d + 0.02
        bezel_z = base_h + body_h * 0.55

        MeshBuilder.add_box(
            bm,
            size=(bezel_w, 0.06, bezel_h),
            offset=(bezel_x, bezel_y, bezel_z),
            mat_idx=casing_mat,
            rgba=(0.78, 0.76, 0.72, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
        )

        # Screen on operator bezel
        MeshBuilder.add_box(
            bm,
            size=(bezel_w * 0.75, 0.015, bezel_h * 0.50),
            offset=(bezel_x, bezel_y - 0.03, bezel_z + bezel_h * 0.15),
            mat_idx=screen_mat,
            rgba=screen_rgba,
            uv_rect=PS1TextureAtlas.get_rect(screen_uv)
        )

        # 3 Keypad buttons below screen
        btn_w = 0.045
        for bi in range(3):
            bx = bezel_x - 0.06 + bi * 0.06
            by = bezel_y - 0.032
            bz = bezel_z - bezel_h * 0.28
            b_uv = "button_white" if bi == 0 else ("button_yellow" if bi == 1 else "button_red")
            MeshBuilder.add_box(
                bm,
                size=(btn_w, 0.012, 0.03),
                offset=(bx, by, bz),
                mat_idx=metal_mat,
                rgba=(0.9, 0.9, 0.9, 1.0),
                uv_rect=PS1TextureAtlas.get_rect(b_uv)
            )

        # Status LED indicator strip
        led_y = bezel_y - 0.032
        led_z = bezel_z + bezel_h * 0.42
        MeshBuilder.add_cylinder(
            bm,
            radius=0.012,
            depth=0.015,
            segments=6,
            offset=(bezel_x, led_y, led_z),
            axis='Y',
            mat_idx=screen_mat,
            rgba=(0.9, 0.8, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect(led_active_uv)
        )

        # -------------------------------------------------------------
        # 3. Motorized Sample Tray & Reaction Vials
        # -------------------------------------------------------------
        tray_w = w * 0.42
        tray_d = d * 0.45
        tray_h = 0.05
        tray_x = half_w * 0.45
        tray_z = base_h + 0.10

        # Ejected tray offset along -Y
        ext_y = self.config.tray_extended
        tray_y = -half_d + tray_d * 0.5 - ext_y

        # Tray housing cavity mouth
        MeshBuilder.add_box(
            bm,
            size=(tray_w + 0.04, 0.02, tray_h + 0.04),
            offset=(tray_x, -half_d + 0.01, tray_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # The slide-out tray plate
        MeshBuilder.add_box(
            bm,
            size=(tray_w, tray_d, tray_h),
            offset=(tray_x, tray_y, tray_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Sample test vials on tray (2x3 grid)
        vial_r = 0.018
        vial_h = 0.08
        for row in range(2):
            for col in range(3):
                vx = tray_x - tray_w * 0.3 + col * (tray_w * 0.3)
                vy = tray_y - tray_d * 0.25 + row * (tray_d * 0.5)
                vz = tray_z + tray_h * 0.5 + vial_h * 0.5

                v_uv = "oxygen_cyan_glow" if (col % 2 == 0) else "cartridge_amber"
                v_rgba = (0.2, 0.8, 0.9, 0.8) if (col % 2 == 0) else (0.9, 0.6, 0.1, 0.8)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=vial_r,
                    depth=vial_h,
                    segments=6,
                    offset=(vx, vy, vz),
                    axis='Z',
                    mat_idx=glass_mat,
                    rgba=v_rgba,
                    uv_rect=PS1TextureAtlas.get_rect(v_uv)
                )

        # -------------------------------------------------------------
        # 4. Thermal Printer Slot & Tape
        # -------------------------------------------------------------
        if self.config.has_thermal_printer:
            pr_x = half_w * 0.25
            pr_y = 0.12
            pr_z = h + 0.005
            # Printer recess
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.08, 0.02),
                offset=(pr_x, pr_y, pr_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Paper output strip
            MeshBuilder.add_box(
                bm,
                size=(0.10, 0.03, 0.015),
                offset=(pr_x, pr_y, pr_z + 0.01),
                mat_idx=casing_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
            )

        # -------------------------------------------------------------
        # 5. Handheld Barcode Scanner Wand & Side Holster
        # -------------------------------------------------------------
        if self.config.has_barcode_scanner:
            wand_x = half_w + 0.03
            wand_y = 0.0
            wand_z = base_h + body_h * 0.45

            # Holster bracket
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.10, 0.12),
                offset=(wand_x, wand_y, wand_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Scanner handle
            MeshBuilder.add_cylinder(
                bm,
                radius=0.018,
                depth=0.14,
                segments=6,
                offset=(wand_x + 0.02, wand_y, wand_z + 0.04),
                axis='Z',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )
            # Scanner optical head
            MeshBuilder.add_box(
                bm,
                size=(0.05, 0.06, 0.04),
                offset=(wand_x + 0.02, wand_y - 0.02, wand_z + 0.12),
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        # -------------------------------------------------------------
        # 6. Rear Cooling Vent Grill
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(w * 0.65, 0.015, body_h * 0.6),
            offset=(0.0, half_d, base_h + body_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
