import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import FuseBoxConfig

class FuseBoxGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for wall-mounted industrial fuse boxes.
    Features stamped steel cabinet, top/bottom conduit knockouts, internal fuse rails
    with ceramic cartridge fuses, hinged door with inspection window, and external cutoff switch.
    """

    def generate(self, config: FuseBoxConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = FuseBoxConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.box_width
        h = self.config.box_height
        d = self.config.box_depth
        half_w = w * 0.5
        half_h = h * 0.5
        wall_th = 0.025

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        ceramic_rgba = (0.92, 0.90, 0.85, 1.0)
        copper_rgba = (0.85, 0.55, 0.20, 1.0)

        # -------------------------------------------------------------
        # 1. Main Cabinet Back and Outer Frame
        # -------------------------------------------------------------
        # In wall_back: Y=0 is back wall, extending into +Y
        # Back panel
        MeshBuilder.add_box(
            bm,
            size=(w, wall_th, h),
            offset=(0.0, wall_th * 0.5, half_h),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Left wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, d, h),
            offset=(-half_w + wall_th * 0.5, d * 0.5, half_h),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Right wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, d, h),
            offset=(half_w - wall_th * 0.5, d * 0.5, half_h),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top wall
        MeshBuilder.add_box(
            bm,
            size=(w, d, wall_th),
            offset=(0.0, d * 0.5, h - wall_th * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Bottom wall
        MeshBuilder.add_box(
            bm,
            size=(w, d, wall_th),
            offset=(0.0, d * 0.5, wall_th * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top/Bottom conduit pipe stub penetrations
        conduit_r = 0.025
        for cx in (-half_w * 0.45, half_w * 0.45):
            # Top conduit
            MeshBuilder.add_cylinder(
                bm,
                radius=conduit_r,
                depth=0.08,
                segments=6,
                offset=(cx, d * 0.5, h + 0.04),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Bottom conduit
            MeshBuilder.add_cylinder(
                bm,
                radius=conduit_r,
                depth=0.08,
                segments=6,
                offset=(cx, d * 0.5, -0.04),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 2. Interior Fuse Rails and Ceramic Fuses
        # -------------------------------------------------------------
        rows = max(1, min(self.config.fuse_rows, 3))
        cols = max(2, min(self.config.fuses_per_row, 5))

        rail_spacing_z = (h - 0.20) / (rows + 1)
        fuse_spacing_x = (w - 0.16) / (cols + 1)

        for ri in range(1, rows + 1):
            rz = ri * rail_spacing_z + 0.08

            # Horizontal DIN rail
            MeshBuilder.add_box(
                bm,
                size=(w - 0.10, 0.015, 0.035),
                offset=(0.0, wall_th + 0.02, rz),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Fuses on rail
            for ci in range(1, cols + 1):
                fx = -half_w + 0.08 + ci * fuse_spacing_x
                fy = wall_th + 0.05

                # Check if this fuse is missing
                is_missing = self.config.missing_fuse and (ri == rows and ci == cols)

                if is_missing:
                    # Just empty copper terminal clips
                    MeshBuilder.add_box(
                        bm,
                        size=(0.025, 0.02, 0.06),
                        offset=(fx, fy, rz),
                        mat_idx=metal_mat,
                        rgba=copper_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
                else:
                    # Ceramic cartridge fuse body
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=0.018,
                        depth=0.075,
                        segments=5,
                        offset=(fx, fy, rz),
                        axis='Z',
                        mat_idx=casing_mat,
                        rgba=ceramic_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
                    )

        # -------------------------------------------------------------
        # 3. Front Hinged Enclosure Door
        # -------------------------------------------------------------
        door_w = w - 0.01
        door_h = h - 0.01
        door_th = 0.025
        hinge_x = -half_w + 0.005
        hinge_y = d

        angle_rad = math.radians(self.config.door_open_angle)
        cos_d = math.cos(angle_rad)
        sin_d = math.sin(angle_rad)

        def rot_door(lx, ly, lz):
            rx = hinge_x + lx * cos_d - ly * sin_d
            ry = hinge_y + lx * sin_d + ly * cos_d
            rz = half_h + lz
            return rx, ry, rz

        # Door panel
        dx, dy, dz = rot_door(door_w * 0.5, door_th * 0.5, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(door_w, door_th, door_h),
            offset=(dx, dy, dz),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Door inspection window
        wx, wy, wz = rot_door(door_w * 0.5, door_th * 0.5 + 0.002, 0.06)
        MeshBuilder.add_box(
            bm,
            size=(door_w * 0.40, door_th + 0.005, door_h * 0.30),
            offset=(wx, wy, wz),
            mat_idx=glass_mat,
            rgba=(0.35, 0.65, 0.75, 0.8),
            uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
        )

        # High-voltage danger warning sign
        sx, sy, sz = rot_door(door_w * 0.5, door_th + 0.005, -door_h * 0.28)
        MeshBuilder.add_box(
            bm,
            size=(0.20, 0.01, 0.16),
            offset=(sx, sy, sz),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("caution_label")
        )

        # Quarter-turn latch handle
        lx, ly, lz = rot_door(door_w - 0.04, door_th + 0.015, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(0.02, 0.03, 0.07),
            offset=(lx, ly, lz),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 4. External Cutoff Switch Box & Lever
        # -------------------------------------------------------------
        if self.config.has_main_switch:
            sw_w = 0.08
            sw_d = d * 0.65
            sw_h = h * 0.45
            sw_x = half_w + sw_w * 0.5
            sw_y = d * 0.5
            sw_z = half_h

            MeshBuilder.add_box(
                bm,
                size=(sw_w, sw_d, sw_h),
                offset=(sw_x, sw_y, sw_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Heavy throw switch lever
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.14,
                segments=6,
                offset=(sw_x + sw_w * 0.5 + 0.02, sw_y, sw_z + 0.02),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Red handle ball
            MeshBuilder.add_cylinder(
                bm,
                radius=0.022,
                depth=0.03,
                segments=6,
                offset=(sw_x + sw_w * 0.5 + 0.02, sw_y, sw_z + 0.08),
                axis='Z',
                mat_idx=accent_mat,
                rgba=(0.9, 0.15, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
