import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CommsAntennaConfig

class CommsAntennaGenerator(BaseAssetGenerator):
    """
    Procedural generator for technical dipole mast antennas.
    Builds tubular central mast, cross dipole elements with ceramic insulators,
    impedance tuning box, coaxial connection ports, and lightning rod spike.
    """

    def generate(self, config: CommsAntennaConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CommsAntennaConfig()

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
        ceramic_rgba = (0.95, 0.82, 0.18, 1.0)

        h = max(1.0, self.config.height)
        r = max(0.02, self.config.mast_radius)

        # -------------------------------------------------------------
        # 1. Base Mounting Flange
        # -------------------------------------------------------------
        flange_r = r * 3.5
        MeshBuilder.add_cylinder(
            bm,
            radius=flange_r,
            depth=0.02,
            segments=7,
            offset=(0.0, 0.0, 0.01),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Flange mounting anchor bolts
        for bi in range(4):
            bang = bi * (math.pi * 0.5)
            bx = math.cos(bang) * (flange_r * 0.72)
            by = math.sin(bang) * (flange_r * 0.72)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.008,
                depth=0.016,
                segments=5,
                offset=(bx, by, 0.02),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 2. Central Tubular Mast
        # -------------------------------------------------------------
        MeshBuilder.add_cylinder(
            bm,
            radius=r,
            depth=h,
            segments=6,
            offset=(0.0, 0.0, h * 0.5),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Base Impedance Tuning Box
        # -------------------------------------------------------------
        if self.config.has_tuning_box:
            box_h = 0.22
            box_w = 0.16
            box_d = 0.14
            MeshBuilder.add_box(
                bm,
                size=(box_w, box_d, box_h),
                offset=(0.0, box_d * 0.5 + r, 0.02 + (box_h * 0.5)),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Coaxial RF connector gland
            MeshBuilder.add_cylinder(
                bm,
                radius=0.014,
                depth=0.03,
                segments=5,
                offset=(0.0, (box_d * 0.5 + r) + (box_d * 0.5) + 0.015, 0.08),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Transverse Dipole Array
        # -------------------------------------------------------------
        tier_count = max(1, self.config.dipole_pairs)
        z_start = h * 0.40
        z_span = h * 0.50
        z_step = z_span / max(1, tier_count)

        arm_len = max(0.15, self.config.arm_length)
        if self.config.antenna_state == "folded":
            arm_len *= 0.4

        for ti in range(tier_count):
            tz = z_start + (ti * z_step)
            # Mast clamp collar
            MeshBuilder.add_cylinder(
                bm,
                radius=r * 1.35,
                depth=0.025,
                segments=6,
                offset=(0.0, 0.0, tz),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Alternating X or Y orientation
            axis = 'X' if (ti % 2 == 0) else 'Y'

            # Broken state: omit or shorten arm on one side
            if self.config.antenna_state == "broken" and ti == 1:
                # Broken stub only
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.008,
                    depth=0.06,
                    segments=5,
                    offset=(0.03, 0.0, tz),
                    axis='X',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                continue

            # Full bilateral dipole arms
            for sign in (-1.0, 1.0):
                arm_half = arm_len * 0.5
                center_offset = sign * (r + (arm_half * 0.5))
                off = (center_offset, 0.0, tz) if axis == 'X' else (0.0, center_offset, tz)

                # Ceramic insulator bead at root
                ins_off = (sign * (r + 0.018), 0.0, tz) if axis == 'X' else (0.0, sign * (r + 0.018), tz)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.014,
                    depth=0.02,
                    segments=5,
                    offset=ins_off,
                    axis=axis,
                    mat_idx=accent_mat,
                    rgba=ceramic_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

                # Dipole conductive element rod
                rod_len = arm_len - 0.03
                rod_mid = sign * (r + 0.025 + (rod_len * 0.5))
                rod_off = (rod_mid, 0.0, tz) if axis == 'X' else (0.0, rod_mid, tz)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.007,
                    depth=rod_len,
                    segments=5,
                    offset=rod_off,
                    axis=axis,
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 5. Top Lightning Arrestor Needle
        # -------------------------------------------------------------
        spike_len = 0.18
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 0.35,
            depth=spike_len,
            segments=5,
            offset=(0.0, 0.0, h + (spike_len * 0.5)),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
