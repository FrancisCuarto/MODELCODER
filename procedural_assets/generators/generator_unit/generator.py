import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import GeneratorUnitConfig

class GeneratorUnitGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for encapsulated auxiliary power generator units.
    Features heavy vibration-isolated skid, sound-attenuated canopy, front radiator louvers,
    top exhaust muffler stack with rain cap, recessed operator panel, and crane lifting eyes.
    """

    def generate(self, config: GeneratorUnitConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = GeneratorUnitConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        len_x = self.config.gen_length
        width_y = self.config.gen_width
        height_z = self.config.gen_height
        half_x = len_x * 0.5
        half_y = width_y * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        # Status
        g_status = self.config.generator_status
        if g_status == "running":
            status_uv = "led_green"
            status_rgba = (0.2, 0.9, 0.3, 1.0)
        elif g_status == "overheat":
            status_uv = "led_yellow"
            status_rgba = (0.95, 0.85, 0.1, 1.0)
        else: # standby / offline
            status_uv = "led_red"
            status_rgba = (0.9, 0.2, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Heavy Skid & Vibration Mounts
        # -------------------------------------------------------------
        skid_h = 0.10
        # Main steel base skid
        MeshBuilder.add_box(
            bm,
            size=(len_x + 0.08, width_y + 0.04, skid_h),
            offset=(0.0, 0.0, skid_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 4 Forklift pockets in skid
        for fx in (-half_x * 0.35, half_x * 0.35):
            MeshBuilder.add_box(
                bm,
                size=(0.18, width_y + 0.06, 0.06),
                offset=(fx, 0.0, skid_h * 0.5),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 2. Sound-Attenuated Canopy Enclosure
        # -------------------------------------------------------------
        canopy_h = height_z - skid_h
        canopy_z = skid_h + canopy_h * 0.5

        # Main acoustic housing block
        MeshBuilder.add_box(
            bm,
            size=(len_x, width_y, canopy_h),
            offset=(0.0, 0.0, canopy_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Front radiator air intake louvers (-X end)
        vent_w = width_y * 0.75
        vent_h = canopy_h * 0.70
        MeshBuilder.add_box(
            bm,
            size=(0.02, vent_w, vent_h),
            offset=(-half_x - 0.005, 0.0, canopy_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        # -------------------------------------------------------------
        # 3. Exhaust Silencer Muffler Stack & Rain Cap
        # -------------------------------------------------------------
        if self.config.has_exhaust_stack:
            muffler_x = -half_x * 0.25
            muffler_y = 0.0
            muffler_r = 0.10
            muffler_len = 0.45

            # Muffler body lying horizontally on roof
            MeshBuilder.add_cylinder(
                bm,
                radius=muffler_r,
                depth=muffler_len,
                segments=8,
                offset=(muffler_x, muffler_y, height_z + muffler_r + 0.02),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Vertical exhaust pipe tail
            pipe_r = 0.045
            pipe_h = 0.28
            pipe_x = muffler_x + muffler_len * 0.5 - 0.05
            pipe_z = height_z + muffler_r * 2.0 + pipe_h * 0.5
            MeshBuilder.add_cylinder(
                bm,
                radius=pipe_r,
                depth=pipe_h,
                segments=6,
                offset=(pipe_x, muffler_y, pipe_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Angled rain flapper cap
            MeshBuilder.add_cylinder(
                bm,
                radius=pipe_r * 1.25,
                depth=0.015,
                segments=6,
                offset=(pipe_x, muffler_y, pipe_z + pipe_h * 0.5 + 0.01),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Rear Operator Control Panel & Instrumentation (+X)
        # -------------------------------------------------------------
        if self.config.has_control_panel:
            pan_x = half_x - 0.02
            pan_w = 0.04
            pan_d = width_y * 0.65
            pan_h = canopy_h * 0.55
            pan_z = canopy_z + 0.05

            # Recessed panel cavity
            MeshBuilder.add_box(
                bm,
                size=(pan_w, pan_d, pan_h),
                offset=(pan_x, 0.0, pan_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Voltmeter & Frequency analog dials
            for di in (-1, 1):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.04,
                    depth=0.02,
                    segments=6,
                    offset=(half_x + 0.005, di * 0.12, pan_z + pan_h * 0.20),
                    axis='X',
                    mat_idx=screen_mat,
                    rgba=(0.95, 0.95, 0.95, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
                )

            # Emergency Stop Button
            MeshBuilder.add_cylinder(
                bm,
                radius=0.03,
                depth=0.025,
                segments=6,
                offset=(half_x + 0.005, -0.12, pan_z - pan_h * 0.22),
                axis='X',
                mat_idx=accent_mat,
                rgba=(0.95, 0.15, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

            # Status run LED
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.015,
                segments=6,
                offset=(half_x + 0.005, 0.12, pan_z - pan_h * 0.22),
                axis='X',
                mat_idx=screen_mat,
                rgba=status_rgba,
                uv_rect=PS1TextureAtlas.get_rect(status_uv)
            )

        # -------------------------------------------------------------
        # 5. Side Maintenance Hatch Doors
        # -------------------------------------------------------------
        if self.config.has_service_hatch:
            for side in (-1.0, 1.0):
                hy = side * (half_y + 0.005)
                # Door outline
                MeshBuilder.add_box(
                    bm,
                    size=(len_x * 0.50, 0.015, canopy_h * 0.70),
                    offset=(0.0, hy, canopy_z - 0.05),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                # Slam latch handle
                MeshBuilder.add_box(
                    bm,
                    size=(0.08, 0.025, 0.03),
                    offset=(0.0, hy + side * 0.01, canopy_z - 0.05),
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # -------------------------------------------------------------
        # 6. Roof Lifting Eye Lugs (4 Corners)
        # -------------------------------------------------------------
        for lx in (-half_x + 0.12, half_x - 0.12):
            for ly in (-half_y + 0.10, half_y - 0.10):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.03,
                    depth=0.04,
                    segments=6,
                    offset=(lx, ly, height_z + 0.02),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
