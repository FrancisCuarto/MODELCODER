import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CoolantPumpConfig

class CoolantPumpGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial centrifugal coolant pump skids.
    Features heavy bedplate skid, finned electric drive motor with terminal box,
    central coupling guard, centrifugal volute casing with flanged ports, dial manometer,
    and isolation valve with handwheel.
    """

    def generate(self, config: CoolantPumpConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CoolantPumpConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        len_x = self.config.pump_length
        width_y = self.config.pump_width
        height_z = self.config.pump_height
        half_x = len_x * 0.5
        half_y = width_y * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        # Status color
        status = self.config.pump_status
        if status == "nominal":
            status_uv = "led_green"
            status_rgba = (0.2, 0.9, 0.3, 1.0)
        elif status == "cavitation":
            status_uv = "led_yellow"
            status_rgba = (0.95, 0.85, 0.1, 1.0)
        else: # offline
            status_uv = "led_red"
            status_rgba = (0.9, 0.2, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Steel Bedplate Skid
        # -------------------------------------------------------------
        skid_h = 0.08
        MeshBuilder.add_box(
            bm,
            size=(len_x, width_y, skid_h),
            offset=(0.0, 0.0, skid_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 4 Corner anchor pads
        for ax in (-half_x + 0.05, half_x - 0.05):
            for ay in (-half_y + 0.05, half_y - 0.05):
                MeshBuilder.add_box(
                    bm,
                    size=(0.07, 0.07, 0.02),
                    offset=(ax, ay, skid_h + 0.01),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 2. Electric Motor Unit (Rear / -X section)
        # -------------------------------------------------------------
        motor_len = len_x * 0.44
        motor_r = width_y * 0.34
        motor_cx = -half_x + 0.08 + motor_len * 0.5
        motor_cz = skid_h + motor_r + 0.04

        # Motor main cylindrical barrel
        MeshBuilder.add_cylinder(
            bm,
            radius=motor_r,
            depth=motor_len,
            segments=8,
            offset=(motor_cx, 0.0, motor_cz),
            axis='X',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # Motor rear cooling fan cowl
        fan_cowl_len = 0.08
        fan_cx = motor_cx - motor_len * 0.5 - fan_cowl_len * 0.5
        MeshBuilder.add_cylinder(
            bm,
            radius=motor_r * 1.02,
            depth=fan_cowl_len,
            segments=8,
            offset=(fan_cx, 0.0, motor_cz),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        # Motor Cooling Fins along body
        fin_count = max(3, min(self.config.motor_fins_count, 7))
        fin_th = 0.015
        fin_proj = 0.03
        for fi in range(fin_count):
            angle = (math.pi * 1.4 * fi) / (fin_count - 1) - math.pi * 0.7
            fx = motor_cx
            fy = math.sin(angle) * (motor_r + fin_proj * 0.5)
            fz = motor_cz + math.cos(angle) * (motor_r + fin_proj * 0.5)

            MeshBuilder.add_box(
                bm,
                size=(motor_len - 0.04, fin_th, fin_proj),
                offset=(fx, fy, fz),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Terminal electrical connection box on top of motor
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.12, 0.09),
            offset=(motor_cx, 0.0, motor_cz + motor_r + 0.045),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Status LED on terminal box
        MeshBuilder.add_cylinder(
            bm,
            radius=0.015,
            depth=0.015,
            segments=6,
            offset=(motor_cx, -0.065, motor_cz + motor_r + 0.045),
            axis='Y',
            mat_idx=screen_mat,
            rgba=status_rgba,
            uv_rect=PS1TextureAtlas.get_rect(status_uv)
        )

        # -------------------------------------------------------------
        # 3. Flexible Coupling Housing (Center)
        # -------------------------------------------------------------
        coupling_len = len_x * 0.12
        coupling_cx = motor_cx + motor_len * 0.5 + coupling_len * 0.5
        MeshBuilder.add_cylinder(
            bm,
            radius=motor_r * 0.65,
            depth=coupling_len,
            segments=8,
            offset=(coupling_cx, 0.0, motor_cz),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 4. Centrifugal Volute Pump Casing (Front / +X)
        # -------------------------------------------------------------
        pump_r = motor_r * 1.15
        pump_th = len_x * 0.26
        pump_cx = coupling_cx + coupling_len * 0.5 + pump_th * 0.5
        pump_cz = motor_cz

        # Volute spiral body (offset 8-sided cylinder)
        MeshBuilder.add_cylinder(
            bm,
            radius=pump_r,
            depth=pump_th,
            segments=8,
            offset=(pump_cx, -0.02, pump_cz),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Axial Suction Port (+X face)
        suct_r = motor_r * 0.55
        suct_len = 0.10
        suct_cx = pump_cx + pump_th * 0.5 + suct_len * 0.5
        MeshBuilder.add_cylinder(
            bm,
            radius=suct_r,
            depth=suct_len,
            segments=6,
            offset=(suct_cx, -0.02, pump_cz),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Suction Flange
        MeshBuilder.add_cylinder(
            bm,
            radius=suct_r * 1.35,
            depth=0.03,
            segments=8,
            offset=(suct_cx + suct_len * 0.5 - 0.015, -0.02, pump_cz),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Vertical Discharge Port (+Z upward)
        disch_r = suct_r * 0.85
        disch_h = 0.20
        disch_cz = pump_cz + pump_r + disch_h * 0.5
        MeshBuilder.add_cylinder(
            bm,
            radius=disch_r,
            depth=disch_h,
            segments=6,
            offset=(pump_cx, -0.02, disch_cz),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Discharge Flange
        MeshBuilder.add_cylinder(
            bm,
            radius=disch_r * 1.35,
            depth=0.03,
            segments=8,
            offset=(pump_cx, -0.02, disch_cz + disch_h * 0.5 - 0.015),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 5. Pressure Dial Manometer & Isolation Handwheel
        # -------------------------------------------------------------
        if self.config.has_pressure_gauge:
            # Gauge stem
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.08,
                segments=6,
                offset=(pump_cx - 0.08, -half_y + 0.08, pump_cz + 0.12),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.85, 0.70, 0.25, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Gauge dial head
            MeshBuilder.add_cylinder(
                bm,
                radius=0.045,
                depth=0.03,
                segments=6,
                offset=(pump_cx - 0.08, -half_y + 0.03, pump_cz + 0.12),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

        if self.config.has_bypass_valve:
            # Valve bonnet block on discharge pipe
            bonnet_z = disch_cz
            MeshBuilder.add_box(
                bm,
                size=(0.08, 0.08, 0.08),
                offset=(pump_cx, -0.02 - disch_r - 0.04, bonnet_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Handwheel spindle
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.08,
                segments=6,
                offset=(pump_cx, -0.02 - disch_r - 0.10, bonnet_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Red handwheel disc
            MeshBuilder.add_cylinder(
                bm,
                radius=0.065,
                depth=0.025,
                segments=6,
                offset=(pump_cx, -0.02 - disch_r - 0.14, bonnet_z),
                axis='Y',
                mat_idx=accent_mat,
                rgba=(0.85, 0.15, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
