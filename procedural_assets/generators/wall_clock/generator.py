import math
from mathutils import Vector
import bpy
import bmesh
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import WallClockConfig

class WallClockGenerator(BaseAssetGenerator[WallClockConfig]):
    """
    Procedural generator for industrial bulkhead 24-hour wall clock.
    Features beveled or octagonal metal casing, analog face with hour/minute ticks,
    geometric 3D hands, center hub cap, protective glass pane, and mounting hardware.
    """

    def generate(self, config: WallClockConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = WallClockConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        accent_rgba = self.material_manager.get_rgba("accent")

        rad = self.config.diameter * 0.5
        depth = self.config.depth
        center_z = rad

        segs = 8

        # 1. Main outer casing bucket
        MeshBuilder.add_cylinder(
            bm,
            radius=rad,
            depth=depth,
            segments=segs,
            offset=(0.0, depth * 0.5, center_z),
            axis='Y',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # 2. Outer front bezel lip / rim
        bezel_thick = 0.015
        MeshBuilder.add_cylinder(
            bm,
            radius=rad * 1.04,
            depth=bezel_thick,
            segments=segs,
            offset=(0.0, depth - bezel_thick * 0.5, center_z),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Cardinal bezel mounting screws / rivets (4 screws)
        for i in range(4):
            ang = i * (math.pi * 0.5) + (math.pi * 0.25)
            bx = math.cos(ang) * (rad * 0.96)
            bz = center_z + math.sin(ang) * (rad * 0.96)
            MeshBuilder.add_box(
                bm,
                size=(0.012, 0.008, 0.012),
                offset=(bx, depth, bz),
                mat_idx=metal_mat,
                rgba=(0.7, 0.72, 0.75, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # 3. Recessed dial face plate
        dial_rad = rad * 0.86
        dial_rgba = (0.92, 0.90, 0.84, 1.0) if self.config.clock_state != "broken" else (0.45, 0.42, 0.38, 1.0)
        MeshBuilder.add_cylinder(
            bm,
            radius=dial_rad,
            depth=0.004,
            segments=segs,
            offset=(0.0, depth - 0.004, center_z),
            axis='Y',
            mat_idx=screen_mat,
            rgba=dial_rgba,
            uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
        )

        # 4. Dial hour markings (4 cardinal main indicators + 4 sub-ticks)
        for i in range(4):
            ang = i * (math.pi * 0.5)
            mark_len = 0.024
            mark_thick = 0.008
            dist = dial_rad * 0.80

            tx = math.cos(ang) * dist
            tz = center_z + math.sin(ang) * dist

            MeshBuilder.add_box(
                bm,
                size=(mark_thick, 0.002, mark_len),
                offset=(tx, depth - 0.001, tz),
                mat_idx=metal_mat,
                rgba=(0.15, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # 5. Center spindle hub cap
        hub_rad = 0.016
        MeshBuilder.add_cylinder(
            bm,
            radius=hub_rad,
            depth=0.012,
            segments=6,
            offset=(0.0, depth + 0.004, center_z),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 6. Hour & Minute Hands
        # Angles in XZ plane (0 deg = 12 o'clock / +Z direction, clockwise rotation)
        hour_val = self.config.hour % 12
        min_val = self.config.minute
        hour_angle_deg = (hour_val + min_val / 60.0) * 30.0
        min_angle_deg = min_val * 6.0

        # Math radians where 0 is +X, so 12 o'clock (+Z) is +pi/2, rotating clockwise subtracts angle
        h_rad = math.pi * 0.5 - math.radians(hour_angle_deg)
        m_rad = math.pi * 0.5 - math.radians(min_angle_deg)

        # Hour Hand (shorter, wider)
        h_len = dial_rad * 0.52
        hx = math.cos(h_rad) * (h_len * 0.5)
        hz = center_z + math.sin(h_rad) * (h_len * 0.5)
        MeshBuilder.add_box(
            bm,
            size=(0.014, 0.004, h_len),
            offset=(hx, depth + 0.003, hz),
            mat_idx=metal_mat,
            rgba=(0.12, 0.12, 0.14, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Minute Hand (longer, slimmer)
        m_len = dial_rad * 0.78
        mx = math.cos(m_rad) * (m_len * 0.5)
        mz = center_z + math.sin(m_rad) * (m_len * 0.5)
        MeshBuilder.add_box(
            bm,
            size=(0.008, 0.004, m_len),
            offset=(mx, depth + 0.006, mz),
            mat_idx=metal_mat,
            rgba=(0.18, 0.18, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Seconds needle (accent red/orange if not broken)
        if self.config.clock_state != "broken":
            s_rad = math.pi * 0.5 - math.radians(25.0 * 6.0)
            s_len = dial_rad * 0.84
            sx = math.cos(s_rad) * (s_len * 0.5)
            sz = center_z + math.sin(s_rad) * (s_len * 0.5)
            MeshBuilder.add_box(
                bm,
                size=(0.004, 0.003, s_len),
                offset=(sx, depth + 0.009, sz),
                mat_idx=accent_mat,
                rgba=(0.85, 0.22, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # 7. Glass Face / Shards
        if self.config.has_glass:
            if self.config.clock_state == "broken":
                # Cracked partial glass segment
                MeshBuilder.add_box(
                    bm,
                    size=(dial_rad * 0.9, 0.003, dial_rad * 0.45),
                    offset=(-dial_rad * 0.2, depth + 0.010, center_z - dial_rad * 0.2),
                    mat_idx=glass_mat,
                    rgba=(0.55, 0.75, 0.85, 0.45),
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )
            else:
                MeshBuilder.add_cylinder(
                    bm,
                    radius=dial_rad * 0.98,
                    depth=0.003,
                    segments=segs,
                    offset=(0.0, depth + 0.010, center_z),
                    axis='Y',
                    mat_idx=glass_mat,
                    rgba=(0.60, 0.80, 0.90, 0.35),
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )

        # 8. Mounting hardware & Top Hanging Tab
        if self.config.has_wall_bracket:
            # Top wall mounting bracket
            bracket_w = 0.04
            bracket_h = 0.035
            bracket_d = 0.012
            MeshBuilder.add_box(
                bm,
                size=(bracket_w, bracket_d, bracket_h),
                offset=(0.0, bracket_d * 0.5, center_z + rad + bracket_h * 0.4),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Bottom electrical / reset knob
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.025,
                segments=6,
                offset=(0.0, depth * 0.5, center_z - rad - 0.012),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        self.finalize_mesh(obj, bm)
        return obj
