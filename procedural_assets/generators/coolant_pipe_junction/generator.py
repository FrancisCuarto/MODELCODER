import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CoolantPipeJunctionConfig

class CoolantPipeJunctionGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial coolant pipe distribution junctions.
    Features 3-way tee or 4-way cross configurations, thermal insulation cladding,
    flanged connections, isolation handwheel valves, and central pressure monitoring gauge.
    """

    def generate(self, config: CoolantPipeJunctionConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CoolantPipeJunctionConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        pipe_r = self.config.pipe_diameter * 0.5
        arm_len = self.config.arm_length
        is_cross = (self.config.junction_type == "cross_4way")

        # Elevation of pipe center above floor
        center_z = 0.55

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        insul_rgba = (0.88, 0.92, 0.95, 1.0)
        brass_rgba = (0.85, 0.70, 0.25, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Floor Support Cradle
        # -------------------------------------------------------------
        cradle_h = center_z - pipe_r - 0.02
        # Base anchor plate
        MeshBuilder.add_box(
            bm,
            size=(0.35, 0.35, 0.02),
            offset=(0.0, 0.0, 0.01),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Vertical pedestal column
        MeshBuilder.add_box(
            bm,
            size=(0.12, 0.12, cradle_h),
            offset=(0.0, 0.0, 0.02 + cradle_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # U-saddle clamp bracket
        MeshBuilder.add_box(
            bm,
            size=(0.28, 0.14, 0.03),
            offset=(0.0, 0.0, center_z - pipe_r),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 2. Central Manifold Hub Block
        # -------------------------------------------------------------
        hub_size = pipe_r * 2.3
        MeshBuilder.add_box(
            bm,
            size=(hub_size, hub_size, hub_size),
            offset=(0.0, 0.0, center_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 3. Main Horizontal Trunk Pipe (X Axis)
        # -------------------------------------------------------------
        # Pipe cylinders
        MeshBuilder.add_cylinder(
            bm,
            radius=pipe_r,
            depth=arm_len * 2.0,
            segments=8,
            offset=(0.0, 0.0, center_z),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Thermal Insulation Jackets on X axis
        if self.config.has_thermal_insulation:
            jack_r = pipe_r * 1.15
            jack_len = arm_len * 0.65
            for sx in (-1, 1):
                jx = sx * (hub_size * 0.5 + jack_len * 0.5 + 0.02)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=jack_r,
                    depth=jack_len,
                    segments=8,
                    offset=(jx, 0.0, center_z),
                    axis='X',
                    mat_idx=casing_mat,
                    rgba=insul_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )
                # Banding straps
                for strap_offset in (-jack_len * 0.35, jack_len * 0.35):
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=jack_r * 1.04,
                        depth=0.02,
                        segments=8,
                        offset=(jx + strap_offset, 0.0, center_z),
                        axis='X',
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                    )

        # Flanges at X extremities
        flange_r = pipe_r * 1.45
        flange_th = 0.035
        for sx in (-1, 1):
            fx = sx * (arm_len - flange_th * 0.5)
            MeshBuilder.add_cylinder(
                bm,
                radius=flange_r,
                depth=flange_th,
                segments=8,
                offset=(fx, 0.0, center_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Transverse Branch Pipes (Y Axis)
        # -------------------------------------------------------------
        y_branches = [1.0] if not is_cross else [1.0, -1.0]

        for sy in y_branches:
            by = sy * (arm_len * 0.5)
            # Branch cylinder
            MeshBuilder.add_cylinder(
                bm,
                radius=pipe_r,
                depth=arm_len,
                segments=8,
                offset=(0.0, by, center_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Insulation jacket
            if self.config.has_thermal_insulation:
                jack_r = pipe_r * 1.15
                jack_len = arm_len * 0.40
                jy = sy * (hub_size * 0.5 + jack_len * 0.5 + 0.02)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=jack_r,
                    depth=jack_len,
                    segments=8,
                    offset=(0.0, jy, center_z),
                    axis='Y',
                    mat_idx=casing_mat,
                    rgba=insul_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )

            # End Flange
            fy = sy * (arm_len - flange_th * 0.5)
            MeshBuilder.add_cylinder(
                bm,
                radius=flange_r,
                depth=flange_th,
                segments=8,
                offset=(0.0, fy, center_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Isolation Gate Valve on branch
            if self.config.has_isolation_valves:
                vy = sy * (arm_len * 0.72)
                # Valve bonnet block
                MeshBuilder.add_box(
                    bm,
                    size=(pipe_r * 2.2, 0.08, pipe_r * 2.2),
                    offset=(0.0, vy, center_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Valve stem
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.015,
                    depth=0.14,
                    segments=6,
                    offset=(0.0, vy, center_z + pipe_r + 0.07),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                # Handwheel
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.075,
                    depth=0.025,
                    segments=6,
                    offset=(0.0, vy, center_z + pipe_r + 0.14),
                    axis='Z',
                    mat_idx=accent_mat,
                    rgba=(0.85, 0.15, 0.1, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("button_red")
                )

        # -------------------------------------------------------------
        # 5. Central Pressure Dial Manometer
        # -------------------------------------------------------------
        if self.config.has_pressure_sensor:
            # Gauge nipple stem
            MeshBuilder.add_cylinder(
                bm,
                radius=0.014,
                depth=0.10,
                segments=6,
                offset=(0.0, 0.0, center_z + hub_size * 0.5 + 0.05),
                axis='Z',
                mat_idx=metal_mat,
                rgba=brass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Gauge dial head
            MeshBuilder.add_cylinder(
                bm,
                radius=0.05,
                depth=0.03,
                segments=6,
                offset=(0.0, -0.015, center_z + hub_size * 0.5 + 0.12),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
