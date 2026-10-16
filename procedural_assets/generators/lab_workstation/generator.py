import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import LabWorkstationConfig

class LabWorkstationGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for modular laboratory chemical workstations.
    Features chemical-resistant benchtop, under-counter drawer units, rear splashback,
    reagent rack shelving, gooseneck wash sink, and swivel telemetry terminal.
    """

    def generate(self, config: LabWorkstationConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = LabWorkstationConfig()

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
        counter_h = 0.90
        counter_th = 0.06

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)
        screen_rgba = (0.2, 0.85, 0.45, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Steel Frame & Legs
        # -------------------------------------------------------------
        leg_w = 0.05
        frame_top_z = counter_h - counter_th
        for lx in (-half_w + 0.04, half_w - 0.04):
            for ly in (-half_d + 0.04, half_d - 0.04):
                MeshBuilder.add_box(
                    bm,
                    size=(leg_w, leg_w, frame_top_z),
                    offset=(lx, ly, frame_top_z * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Leveling foot pad
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.035,
                    depth=0.02,
                    segments=6,
                    offset=(lx, ly, 0.01),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # Bottom tie bars
        for lx in (-half_w + 0.04, half_w - 0.04):
            MeshBuilder.add_box(
                bm,
                size=(leg_w, d - 0.08, 0.04),
                offset=(lx, 0.0, 0.12),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        MeshBuilder.add_box(
            bm,
            size=(w - 0.08, leg_w, 0.04),
            offset=(0.0, half_d - 0.04, 0.12),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Main Chemical-Resistant Countertop
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(w, d, counter_th),
            offset=(0.0, 0.0, counter_h - counter_th * 0.5),
            mat_idx=casing_mat,
            rgba=(0.92, 0.93, 0.95, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
        )

        # Rear Splashback Wall
        splash_h = 0.35
        MeshBuilder.add_box(
            bm,
            size=(w, 0.03, splash_h),
            offset=(0.0, half_d - 0.015, counter_h + splash_h * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # -------------------------------------------------------------
        # 3. Under-Counter Drawer Pedestals
        # -------------------------------------------------------------
        drawer_count = max(1, min(self.config.drawer_units, 3))
        pedestal_w = min(0.42, (w - 0.2) / drawer_count)
        pedestal_d = d - 0.10
        pedestal_h = counter_h - counter_th - 0.14

        for di in range(drawer_count):
            if drawer_count == 1:
                ped_x = -half_w + 0.10 + pedestal_w * 0.5
            elif drawer_count == 2:
                ped_x = (-half_w + 0.10 + pedestal_w * 0.5) if di == 0 else (half_w - 0.10 - pedestal_w * 0.5)
            else:
                ped_x = -half_w + 0.10 + di * (pedestal_w + 0.08) + pedestal_w * 0.5

            ped_z = 0.12 + pedestal_h * 0.5
            # Drawer box body
            MeshBuilder.add_box(
                bm,
                size=(pedestal_w, pedestal_d, pedestal_h),
                offset=(ped_x, 0.0, ped_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # 3 Drawer faces & handles
            df_h = (pedestal_h - 0.04) / 3.0
            for fi in range(3):
                df_z = 0.12 + 0.02 + fi * df_h + df_h * 0.5
                MeshBuilder.add_box(
                    bm,
                    size=(pedestal_w - 0.04, 0.015, df_h - 0.02),
                    offset=(ped_x, -half_d + 0.045, df_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                # Pull handle
                MeshBuilder.add_box(
                    bm,
                    size=(0.10, 0.02, 0.02),
                    offset=(ped_x, -half_d + 0.03, df_z),
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # -------------------------------------------------------------
        # 4. Wash Basin & Gooseneck Faucet
        # -------------------------------------------------------------
        if self.config.has_sink:
            sink_w = 0.35
            sink_d = 0.35
            sink_x = half_w - sink_w * 0.5 - 0.08
            sink_y = -0.04
            # Sink rim bezel
            MeshBuilder.add_box(
                bm,
                size=(sink_w, sink_d, 0.02),
                offset=(sink_x, sink_y, counter_h + 0.01),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Drain depression
            MeshBuilder.add_cylinder(
                bm,
                radius=0.04,
                depth=0.015,
                segments=6,
                offset=(sink_x, sink_y, counter_h + 0.005),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Gooseneck faucet vertical tube
            faucet_x = sink_x
            faucet_y = sink_y + sink_d * 0.5 - 0.04
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.28,
                segments=6,
                offset=(faucet_x, faucet_y, counter_h + 0.14),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Curved spout forward
            MeshBuilder.add_box(
                bm,
                size=(0.025, 0.10, 0.025),
                offset=(faucet_x, faucet_y - 0.04, counter_h + 0.28),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 5. Reagent Rack Shelving
        # -------------------------------------------------------------
        if self.config.has_upper_shelf:
            shelf_w = w - 0.10
            shelf_d = 0.22
            shelf_z1 = counter_h + 0.45
            shelf_z2 = counter_h + 0.75

            # Vertical shelf struts
            for sx in (-half_w + 0.08, half_w - 0.08):
                MeshBuilder.add_box(
                    bm,
                    size=(0.04, 0.04, 0.85),
                    offset=(sx, half_d - shelf_d * 0.5, counter_h + 0.425),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

            # Two shelves
            for sz in (shelf_z1, shelf_z2):
                MeshBuilder.add_box(
                    bm,
                    size=(shelf_w, shelf_d, 0.025),
                    offset=(0.0, half_d - shelf_d * 0.5, sz),
                    mat_idx=casing_mat,
                    rgba=casing_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )
                # Front retainer wire lip
                MeshBuilder.add_box(
                    bm,
                    size=(shelf_w, 0.015, 0.04),
                    offset=(0.0, half_d - shelf_d + 0.01, sz + 0.02),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

            # Reagent bottle cassettes on shelf 1
            for bi in range(4):
                bx = -shelf_w * 0.35 + bi * 0.16
                by = half_d - shelf_d * 0.5
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.035,
                    depth=0.12,
                    segments=6,
                    offset=(bx, by, shelf_z1 + 0.012 + 0.06),
                    axis='Z',
                    mat_idx=glass_mat,
                    rgba=(0.85, 0.65, 0.2, 0.85),
                    uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                )

        # -------------------------------------------------------------
        # 6. Swivel Telemetry CRT Terminal Arm
        # -------------------------------------------------------------
        if self.config.has_terminal_screen:
            t_x = -half_w + 0.20
            t_y = half_d - 0.18
            t_z = counter_h + 0.40

            # Mounting arm stalk
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=0.35,
                segments=6,
                offset=(t_x, t_y, counter_h + 0.175),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # CRT box
            MeshBuilder.add_box(
                bm,
                size=(0.24, 0.18, 0.20),
                offset=(t_x, t_y - 0.10, t_z),
                mat_idx=casing_mat,
                rgba=(0.78, 0.76, 0.72, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )
            # CRT screen surface
            MeshBuilder.add_box(
                bm,
                size=(0.18, 0.015, 0.14),
                offset=(t_x, t_y - 0.19, t_z),
                mat_idx=screen_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
