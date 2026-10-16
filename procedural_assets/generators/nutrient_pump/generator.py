import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import NutrientPumpConfig

class NutrientPumpGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial nutrient dosing pumps.
    Builds vibration-isolated baseplate, finned electric stator motor, centrifugal impeller volute,
    inline translucent filter canister, and discharge pressure dial.
    """

    def generate(self, config: NutrientPumpConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = NutrientPumpConfig()

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
        green_rgba = (0.22, 0.85, 0.40, 1.0)
        dial_rgba = (0.90, 0.90, 0.92, 1.0)

        scale = max(0.3, self.config.pump_size)
        base_w = scale * 1.05
        base_d = scale * 0.65
        center_z = 0.03 + (scale * 0.32)

        # -------------------------------------------------------------
        # 1. Base Mounting Skid & Vibration Isolation Pucks
        # -------------------------------------------------------------
        # Steel channel baseplate
        MeshBuilder.add_box(
            bm,
            size=(base_w, base_d, 0.02),
            offset=(0.0, 0.0, 0.02),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # 4 Neoprene damping foot pucks
        for px in (-base_w * 0.42, base_w * 0.42):
            for py in (-base_d * 0.38, base_d * 0.38):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.022,
                    depth=0.015,
                    segments=6,
                    offset=(px, py, 0.0075),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=(0.14, 0.14, 0.16, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # -------------------------------------------------------------
        # 2. Electric Drive Motor (Left side)
        # -------------------------------------------------------------
        motor_x = -base_w * 0.20
        motor_r = scale * 0.22
        motor_l = scale * 0.45

        # Motor stator barrel
        MeshBuilder.add_cylinder(
            bm,
            radius=motor_r,
            depth=motor_l,
            segments=7,
            offset=(motor_x, 0.0, center_z),
            axis='X',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Rear cooling fan cowl
        MeshBuilder.add_cylinder(
            bm,
            radius=motor_r * 0.95,
            depth=0.05,
            segments=7,
            offset=(motor_x - (motor_l * 0.5) - 0.025, 0.0, center_z),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )
        # Top electrical conduit connection box
        MeshBuilder.add_box(
            bm,
            size=(0.08, 0.08, 0.06),
            offset=(motor_x, 0.0, center_z + motor_r + 0.03),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 3. Centrifugal Pump Volute (Center)
        # -------------------------------------------------------------
        pump_x = motor_x + (motor_l * 0.5) + 0.06
        volute_r = motor_r * 1.25
        volute_w = scale * 0.16

        # Volute impeller chamber
        MeshBuilder.add_cylinder(
            bm,
            radius=volute_r,
            depth=volute_w,
            segments=8,
            offset=(pump_x, 0.0, center_z),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Upward discharge outlet nozzle
        nozzle_h = scale * 0.22
        MeshBuilder.add_cylinder(
            bm,
            radius=0.03,
            depth=nozzle_h,
            segments=6,
            offset=(pump_x, 0.0, center_z + volute_r + (nozzle_h * 0.5)),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 4. Inline Filter Canister (Right side)
        # -------------------------------------------------------------
        if self.config.has_filter_canister:
            filter_x = pump_x + 0.14
            filter_r = scale * 0.15
            filter_h = scale * 0.38

            # Upper manifold head
            MeshBuilder.add_cylinder(
                bm,
                radius=filter_r * 1.1,
                depth=0.04,
                segments=7,
                offset=(filter_x, 0.0, center_z + (filter_h * 0.45)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Translucent nutrient filter bowl
            MeshBuilder.add_cylinder(
                bm,
                radius=filter_r,
                depth=filter_h,
                segments=7,
                offset=(filter_x, 0.0, center_z),
                axis='Z',
                mat_idx=accent_mat,
                rgba=green_rgba,
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )

        # -------------------------------------------------------------
        # 5. Pressure Dial Gauge
        # -------------------------------------------------------------
        if self.config.has_pressure_dial:
            gauge_z = center_z + volute_r + nozzle_h
            # Dial circular body
            MeshBuilder.add_cylinder(
                bm,
                radius=0.032,
                depth=0.016,
                segments=7,
                offset=(pump_x, 0.04, gauge_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=dial_rgba,
                uv_rect=PS1TextureAtlas.get_rect("button_white")
            )
            # Pointer needle
            MeshBuilder.add_box(
                bm,
                size=(0.005, 0.006, 0.024),
                offset=(pump_x, 0.05, gauge_z),
                mat_idx=accent_mat,
                rgba=(0.95, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
