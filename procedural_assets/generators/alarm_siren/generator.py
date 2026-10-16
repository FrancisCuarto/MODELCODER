import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import AlarmSirenConfig

class AlarmSirenGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial alarm sirens and evacuation strobes.
    Builds waterproof junction box with mounting ears, acoustic trumpet horns,
    cylindrical Fresnel strobe beacon, protective wire guard cage, and conduit connectors.
    """

    def generate(self, config: AlarmSirenConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = AlarmSirenConfig()

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

        color_map = {
            "red": (0.95, 0.12, 0.12, 1.0),
            "amber": (0.95, 0.65, 0.10, 1.0),
            "blue": (0.15, 0.45, 0.95, 1.0)
        }
        strobe_rgba = color_map.get(self.config.strobe_color, color_map["red"])
        if not self.config.is_active:
            strobe_rgba = (0.20, 0.20, 0.22, 1.0)

        box_w = 0.18
        box_d = 0.10
        box_h = 0.20
        half_w = box_w * 0.5
        half_h = box_h * 0.5

        # -------------------------------------------------------------
        # 1. Main Die-Cast Junction Box
        # -------------------------------------------------------------
        # Wall base backplate with 4 corner mounting tabs
        MeshBuilder.add_box(
            bm,
            size=(box_w + 0.04, 0.015, box_h + 0.04),
            offset=(0.0, 0.0075, 0.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )
        # Main housing body (high-visibility safety paint)
        MeshBuilder.add_box(
            bm,
            size=(box_w, box_d, box_h),
            offset=(0.0, 0.015 + (box_d * 0.5), 0.0),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        front_y = 0.015 + box_d

        # -------------------------------------------------------------
        # 2. Acoustic Trumpet Horn(s)
        # -------------------------------------------------------------
        horn_z = -0.03
        if self.config.siren_type == "dual_horn":
            # Dual horn array (left & right flaring bells)
            for hx in (-0.055, 0.055):
                # Horn driver neck
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.028,
                    depth=0.04,
                    segments=6,
                    offset=(hx, front_y + 0.02, horn_z),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Flared mouth bell
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.046,
                    depth=0.06,
                    segments=6,
                    offset=(hx, front_y + 0.07, horn_z),
                    axis='Y',
                    mat_idx=casing_mat,
                    rgba=casing_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )
        else:
            # Single large center acoustic horn
            # Driver neck
            MeshBuilder.add_cylinder(
                bm,
                radius=0.036,
                depth=0.05,
                segments=7,
                offset=(0.0, front_y + 0.025, horn_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Flared mouth bell
            MeshBuilder.add_cylinder(
                bm,
                radius=0.068,
                depth=0.07,
                segments=7,
                offset=(0.0, front_y + 0.085, horn_z),
                axis='Y',
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Internal audio phase plug bullet
            MeshBuilder.add_cylinder(
                bm,
                radius=0.016,
                depth=0.03,
                segments=5,
                offset=(0.0, front_y + 0.09, horn_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 3. Strobe Beacon Lens (Top of box)
        # -------------------------------------------------------------
        beacon_base_z = half_h + 0.005
        beacon_radius = 0.042
        beacon_h = 0.065
        beacon_center_y = 0.015 + (box_d * 0.5)

        # Chrome reflector mounting ring
        MeshBuilder.add_cylinder(
            bm,
            radius=beacon_radius + 0.008,
            depth=0.014,
            segments=7,
            offset=(0.0, beacon_center_y, beacon_base_z + 0.007),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Faceted translucent strobe dome
        MeshBuilder.add_cylinder(
            bm,
            radius=beacon_radius,
            depth=beacon_h,
            segments=7,
            offset=(0.0, beacon_center_y, beacon_base_z + 0.014 + (beacon_h * 0.5)),
            axis='Z',
            mat_idx=accent_mat,
            rgba=strobe_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # -------------------------------------------------------------
        # 4. Protective Wire Guard Cage
        # -------------------------------------------------------------
        if self.config.has_wire_guard:
            cage_top_z = beacon_base_z + 0.014 + beacon_h + 0.015
            cage_r = beacon_radius + 0.015
            # Top hoop ring
            MeshBuilder.add_cylinder(
                bm,
                radius=cage_r,
                depth=0.008,
                segments=6,
                offset=(0.0, beacon_center_y, cage_top_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # 4 vertical wire ribs
            wire_h = beacon_h + 0.02
            for ax, ay in ((-cage_r, 0.0), (cage_r, 0.0), (0.0, -cage_r), (0.0, cage_r)):
                MeshBuilder.add_box(
                    bm,
                    size=(0.006, 0.006, wire_h),
                    offset=(ax, beacon_center_y + ay, beacon_base_z + 0.01 + (wire_h * 0.5)),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 5. Top Conduit Pipe Entry
        # -------------------------------------------------------------
        MeshBuilder.add_cylinder(
            bm,
            radius=0.014,
            depth=0.035,
            segments=5,
            offset=(0.06, beacon_center_y, half_h + 0.018),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
