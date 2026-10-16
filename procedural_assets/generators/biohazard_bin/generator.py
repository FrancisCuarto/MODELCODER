import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import BiohazardBinConfig

class BiohazardBinGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for clinical biohazard waste bins with foot-pedal lid.
    Features octagonal stamped canister, mechanical pedal linkage, biohazard liner bag,
    hinged lid with grip handle, side carrying handles, and warning placards.
    """

    def generate(self, config: BiohazardBinConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = BiohazardBinConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        radius = self.config.bin_diameter * 0.5
        h = self.config.bin_height
        body_h = h * 0.88
        segments = 8

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        accent_rgba = self.material_manager.get_rgba("accent")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        # -------------------------------------------------------------
        # 1. Base Ring & Non-slip Rubber Collar
        # -------------------------------------------------------------
        base_h = 0.05
        MeshBuilder.add_cylinder(
            bm,
            radius=radius * 1.05,
            depth=base_h,
            segments=segments,
            offset=(0.0, 0.0, base_h * 0.5),
            axis='Z',
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # -------------------------------------------------------------
        # 2. Main Octagonal Bin Body
        # -------------------------------------------------------------
        body_center_z = base_h + body_h * 0.5
        MeshBuilder.add_cylinder(
            bm,
            radius=radius,
            depth=body_h,
            segments=segments,
            offset=(0.0, 0.0, body_center_z),
            axis='Z',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("red_paint_worn")
        )

        # -------------------------------------------------------------
        # 3. Foot Pedal Mechanism & Rear Linkage
        # -------------------------------------------------------------
        if self.config.has_foot_pedal:
            pedal_y = -radius - 0.08
            pedal_z = 0.035
            # Foot lever
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.12, 0.02),
                offset=(0.0, pedal_y, pedal_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Rubber pad on pedal
            MeshBuilder.add_box(
                bm,
                size=(0.10, 0.06, 0.01),
                offset=(0.0, pedal_y, pedal_z + 0.012),
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

            # Rear vertical rod
            rod_h = body_h + 0.04
            MeshBuilder.add_box(
                bm,
                size=(0.02, 0.02, rod_h),
                offset=(0.0, radius + 0.015, base_h + rod_h * 0.5),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Hinge bracket
            MeshBuilder.add_box(
                bm,
                size=(0.08, 0.04, 0.05),
                offset=(0.0, radius + 0.015, base_h + body_h),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Inner Bag Lip / Liner
        # -------------------------------------------------------------
        rim_top_z = base_h + body_h
        if self.config.has_inner_bag_lip:
            bag_lip_h = 0.04
            MeshBuilder.add_cylinder(
                bm,
                radius=radius * 1.03,
                depth=bag_lip_h,
                segments=segments,
                offset=(0.0, 0.0, rim_top_z - bag_lip_h * 0.5),
                axis='Z',
                mat_idx=accent_mat,
                rgba=accent_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # -------------------------------------------------------------
        # 5. Hinged Lid & Handle
        # -------------------------------------------------------------
        lid_th = 0.04
        lid_radius = radius * 1.06
        hinge_pivot_y = radius
        hinge_pivot_z = rim_top_z + 0.01

        lid_angle_rad = math.radians(max(0.0, min(self.config.lid_open_angle, 75.0)))
        cos_l = math.cos(lid_angle_rad)
        sin_l = math.sin(lid_angle_rad)

        # Lid center position rotated around rear hinge
        # In unrotated space, lid center is at (0.0, 0.0, rim_top_z + 0.01 + lid_th*0.5)
        # Offset from hinge: dy = -hinge_pivot_y, dz = lid_th*0.5
        dy_rot = -hinge_pivot_y * cos_l - (lid_th * 0.5) * sin_l
        dz_rot = -hinge_pivot_y * (-sin_l) + (lid_th * 0.5) * cos_l
        lid_cx = 0.0
        lid_cy = hinge_pivot_y + dy_rot
        lid_cz = hinge_pivot_z + dz_rot

        MeshBuilder.add_cylinder(
            bm,
            radius=lid_radius,
            depth=lid_th,
            segments=segments,
            offset=(lid_cx, lid_cy, lid_cz),
            axis='Z',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("red_paint_worn")
        )

        # Grip handle on lid
        h_dy_rot = -hinge_pivot_y * cos_l - (lid_th + 0.015) * sin_l
        h_dz_rot = -hinge_pivot_y * (-sin_l) + (lid_th + 0.015) * cos_l
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.035, 0.03),
            offset=(0.0, hinge_pivot_y + h_dy_rot, hinge_pivot_z + h_dz_rot),
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # -------------------------------------------------------------
        # 6. Side Carrying Handles
        # -------------------------------------------------------------
        if self.config.has_side_handles:
            handle_z = body_center_z + 0.08
            for side in (-1.0, 1.0):
                MeshBuilder.add_box(
                    bm,
                    size=(0.025, 0.12, 0.035),
                    offset=(side * (radius + 0.02), 0.0, handle_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 7. Front Hazard Placard
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(0.18, 0.015, 0.18),
            offset=(0.0, -radius - 0.005, body_center_z),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("caution_label")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
