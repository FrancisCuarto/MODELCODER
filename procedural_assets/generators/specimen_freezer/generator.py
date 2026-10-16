import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SpecimenFreezerConfig

class SpecimenFreezerGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for cryogenic specimen freezers (-80°C).
    Features heavy insulated cabinet, compressor intake grill, slide-out internal
    cryo-trays, vacuum latch handle, digital readout display, and triple-pane window.
    """

    def generate(self, config: SpecimenFreezerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = SpecimenFreezerConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.freezer_width
        d = self.config.freezer_depth
        h = self.config.freezer_height
        half_w = w * 0.5
        half_d = d * 0.5

        wall_th = 0.08
        plinth_h = 0.35

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)
        screen_rgba = (0.2, 0.85, 0.35, 1.0) if self.config.temperature_celsius <= -50.0 else (0.9, 0.65, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Base Plinth & Compressor Vent
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(w, d, plinth_h),
            offset=(0.0, 0.0, plinth_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        vent_w = w * 0.75
        vent_h = plinth_h * 0.65
        MeshBuilder.add_box(
            bm,
            size=(vent_w, 0.02, vent_h),
            offset=(0.0, -half_d - 0.005, plinth_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        # -------------------------------------------------------------
        # 2. Main Insulated Body Walls
        # -------------------------------------------------------------
        body_h = h - plinth_h
        body_center_z = plinth_h + body_h * 0.5

        # Back wall
        MeshBuilder.add_box(
            bm,
            size=(w, wall_th, body_h),
            offset=(0.0, half_d - wall_th * 0.5, body_center_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Left wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, d - wall_th, body_h),
            offset=(-half_w + wall_th * 0.5, 0.0, body_center_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Right wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, d - wall_th, body_h),
            offset=(half_w - wall_th * 0.5, 0.0, body_center_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top ceiling
        MeshBuilder.add_box(
            bm,
            size=(w, d, wall_th),
            offset=(0.0, 0.0, h - wall_th * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Floor of cold chamber
        MeshBuilder.add_box(
            bm,
            size=(w - wall_th * 2, d - wall_th * 2, wall_th),
            offset=(0.0, 0.0, plinth_h + wall_th * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Perimeter rubber gasket trim
        MeshBuilder.add_box(
            bm,
            size=(w - 0.02, 0.02, body_h - 0.02),
            offset=(0.0, -half_d + 0.01, body_center_z),
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # -------------------------------------------------------------
        # 3. Interior Cryogenic Shelves & Cassette Boxes
        # -------------------------------------------------------------
        tray_count = max(2, min(self.config.tray_count, 6))
        inner_w = w - wall_th * 2 - 0.04
        inner_d = d - wall_th * 2 - 0.06
        chamber_avail_h = body_h - wall_th * 2 - 0.08
        tray_spacing = chamber_avail_h / (tray_count + 1)

        for i in range(1, tray_count + 1):
            tray_z = plinth_h + wall_th + i * tray_spacing
            MeshBuilder.add_box(
                bm,
                size=(inner_w, inner_d, 0.02),
                offset=(0.0, 0.02, tray_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            box_w = inner_w * 0.38
            box_d = inner_d * 0.65
            box_h = min(0.12, tray_spacing * 0.6)
            for bx_side in (-1.0, 1.0):
                bx = bx_side * (box_w * 0.6)
                box_uv = "cartridge_amber" if (i % 2 == 0) else "metal_dark_grime"
                MeshBuilder.add_box(
                    bm,
                    size=(box_w, box_d, box_h),
                    offset=(bx, 0.02, tray_z + 0.01 + box_h * 0.5),
                    mat_idx=metal_mat,
                    rgba=(0.7, 0.55, 0.25, 1.0) if (i % 2 == 0) else metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect(box_uv)
                )

        # -------------------------------------------------------------
        # 4. Front Insulated Heavy Door & Latch
        # -------------------------------------------------------------
        door_w = w - 0.04
        door_h = body_h - 0.04
        door_th = 0.09
        hinge_x = -half_w + 0.02
        hinge_y = -half_d

        angle_rad = math.radians(self.config.door_open_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        def rotate_door_pt(lx, ly, lz):
            rx = hinge_x + lx * cos_a - ly * sin_a
            ry = hinge_y + lx * sin_a + ly * cos_a
            rz = body_center_z + lz
            return rx, ry, rz

        # Door slab center
        dx, dy, dz = rotate_door_pt(door_w * 0.5, -door_th * 0.5, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(door_w, door_th, door_h),
            offset=(dx, dy, dz),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Inspection Window
        if self.config.has_window:
            wx, wy, wz = rotate_door_pt(door_w * 0.5, -door_th * 0.5 - 0.005, door_h * 0.12)
            MeshBuilder.add_box(
                bm,
                size=(door_w * 0.38, door_th + 0.01, door_h * 0.32),
                offset=(wx, wy, wz),
                mat_idx=glass_mat,
                rgba=(0.4, 0.65, 0.75, 0.8),
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )

        # Heavy Vacuum Clamp Latch & Handle
        lx, ly, lz = rotate_door_pt(door_w - 0.08, -door_th - 0.04, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(0.05, 0.08, 0.32),
            offset=(lx, ly, lz),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        hx, hy, hz = rotate_door_pt(door_w - 0.08, -door_th - 0.08, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(0.03, 0.03, 0.40),
            offset=(hx, hy, hz),
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # Digital Readout Bezel & Screen
        rx, ry, rz = rotate_door_pt(door_w * 0.5, -door_th - 0.015, door_h * 0.38)
        MeshBuilder.add_box(
            bm,
            size=(0.26, 0.02, 0.12),
            offset=(rx, ry, rz),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        screen_uv = "crt_screen_green" if self.config.temperature_celsius <= -50.0 else "crt_screen_amber"
        sx, sy, sz = rotate_door_pt(door_w * 0.5, -door_th - 0.025, door_h * 0.38)
        MeshBuilder.add_box(
            bm,
            size=(0.20, 0.015, 0.07),
            offset=(sx, sy, sz),
            mat_idx=screen_mat,
            rgba=screen_rgba,
            uv_rect=PS1TextureAtlas.get_rect(screen_uv)
        )

        # Caution label on lower door
        cx, cy, cz = rotate_door_pt(door_w * 0.5, -door_th - 0.01, -door_h * 0.28)
        MeshBuilder.add_box(
            bm,
            size=(0.22, 0.015, 0.18),
            offset=(cx, cy, cz),
            mat_idx=metal_mat,
            rgba=(0.9, 0.8, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("caution_label")
        )

        # -------------------------------------------------------------
        # 5. Top Emergency Alarm Beacon (Optional)
        # -------------------------------------------------------------
        if self.config.has_alarm_beacon or self.config.temperature_celsius > -20.0:
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.14, 0.04),
                offset=(0.0, 0.0, h + 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            MeshBuilder.add_cylinder(
                bm,
                radius=0.06,
                depth=0.12,
                segments=6,
                offset=(0.0, 0.0, h + 0.08),
                axis='Z',
                mat_idx=screen_mat,
                rgba=(0.95, 0.15, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("led_red")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
