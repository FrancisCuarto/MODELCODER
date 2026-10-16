import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import EmergencyBeaconConfig

class EmergencyBeaconGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial hazard and emergency rotating beacons.
    Builds circular mounting flange or pedestal post, internal parabolic reflector cup,
    faceted colored polycarbonate lens, and protective steel wire cage.
    """

    def generate(self, config: EmergencyBeaconConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = EmergencyBeaconConfig()

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
            "amber": (0.95, 0.70, 0.10, 1.0),
            "red": (0.95, 0.15, 0.15, 1.0),
            "blue": (0.15, 0.45, 0.95, 1.0),
            "green": (0.15, 0.90, 0.25, 1.0)
        }
        lens_rgba = color_map.get(self.config.beacon_color, color_map["amber"])
        if not self.config.is_active:
            lens_rgba = (0.22, 0.22, 0.25, 1.0)

        # -------------------------------------------------------------
        # 1. Base Mounting (Flange or Pedestal Post)
        # -------------------------------------------------------------
        base_z = 0.0
        if self.config.base_style == "pedestal":
            pole_h = 0.40
            # Floor circular base flange
            MeshBuilder.add_cylinder(
                bm,
                radius=0.10,
                depth=0.02,
                segments=8,
                offset=(0.0, 0.0, 0.01),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Vertical standpipe
            MeshBuilder.add_cylinder(
                bm,
                radius=0.026,
                depth=pole_h,
                segments=6,
                offset=(0.0, 0.0, 0.02 + (pole_h * 0.5)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            base_z = 0.02 + pole_h
        else:
            # Low-profile direct flange
            base_z = 0.0

        # Beacon collar base casting
        collar_r = 0.082
        collar_h = 0.045
        MeshBuilder.add_cylinder(
            bm,
            radius=collar_r,
            depth=collar_h,
            segments=8,
            offset=(0.0, 0.0, base_z + (collar_h * 0.5)),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Peripheral mounting bolts
        for bi in range(4):
            bar_ang = bi * (math.pi * 0.5)
            bx = math.cos(bar_ang) * (collar_r - 0.012)
            by = math.sin(bar_ang) * (collar_r - 0.012)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.007,
                depth=0.014,
                segments=5,
                offset=(bx, by, base_z + collar_h + 0.004),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 2. Internal Rotational Reflector Cup
        # -------------------------------------------------------------
        lens_bottom_z = base_z + collar_h
        MeshBuilder.add_box(
            bm,
            size=(0.045, 0.025, 0.06),
            offset=(0.01, 0.0, lens_bottom_z + 0.04),
            mat_idx=metal_mat,
            rgba=(0.85, 0.85, 0.90, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Translucent Polycarbonate Lens
        # -------------------------------------------------------------
        lens_r = 0.068
        lens_h = 0.125
        MeshBuilder.add_cylinder(
            bm,
            radius=lens_r,
            depth=lens_h,
            segments=8,
            offset=(0.0, 0.0, lens_bottom_z + (lens_h * 0.5)),
            axis='Z',
            mat_idx=accent_mat,
            rgba=lens_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )
        # Dome top cap
        MeshBuilder.add_cylinder(
            bm,
            radius=lens_r * 0.82,
            depth=0.02,
            segments=8,
            offset=(0.0, 0.0, lens_bottom_z + lens_h + 0.01),
            axis='Z',
            mat_idx=accent_mat,
            rgba=lens_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # -------------------------------------------------------------
        # 4. Protective Steel Wire Cage
        # -------------------------------------------------------------
        if self.config.has_protective_cage:
            cage_r = lens_r + 0.016
            cage_top_z = lens_bottom_z + lens_h + 0.03
            wire_h = lens_h + 0.03

            # Top ring guard
            MeshBuilder.add_cylinder(
                bm,
                radius=cage_r,
                depth=0.010,
                segments=8,
                offset=(0.0, 0.0, cage_top_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # 4 Vertical wire struts
            for ci in range(4):
                c_ang = ci * (math.pi * 0.5) + (math.pi * 0.25)
                cx = math.cos(c_ang) * cage_r
                cy = math.sin(c_ang) * cage_r
                MeshBuilder.add_box(
                    bm,
                    size=(0.008, 0.008, wire_h),
                    offset=(cx, cy, lens_bottom_z + (wire_h * 0.5)),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
