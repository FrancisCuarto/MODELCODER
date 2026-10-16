import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import BiometricScannerConfig

class BiometricScannerGenerator(BaseAssetGenerator):
    """
    Procedural generator for high-security biometric identification scanners (palm / fingerprint).
    Builds sloped ergonomic enclosure, illuminated glass palm platen, laser scan sweep emitter,
    facial/retina recognition optics, intercom audio louvers, and wall or floor pedestal mount.
    """

    def generate(self, config: BiometricScannerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = BiometricScannerConfig()

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

        laser_colors = {
            "active_laser": (0.15, 0.90, 0.95, 1.0),
            "verified": (0.20, 0.95, 0.25, 1.0),
            "alarm": (0.95, 0.15, 0.15, 1.0),
            "idle": (0.15, 0.28, 0.32, 1.0)
        }
        laser_rgba = laser_colors.get(self.config.scan_state, laser_colors["active_laser"])

        w = 0.24
        h = 0.34
        d = 0.08
        half_w = w * 0.5
        half_h = h * 0.5

        is_pedestal = self.config.mount_style == "pedestal"
        head_z = 1.05 if is_pedestal else 0.0

        # -------------------------------------------------------------
        # 1. Main Terminal Enclosure Box
        # -------------------------------------------------------------
        # Rear housing box
        MeshBuilder.add_box(
            bm,
            size=(w, d, h),
            offset=(0.0, d * 0.5, head_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        front_y = d

        # -------------------------------------------------------------
        # 2. Lower Palm / Fingerprint Scanner Platen
        # -------------------------------------------------------------
        platen_w = 0.15
        platen_h = 0.15
        platen_z = head_z - 0.06

        # Recessed scanner bezel frame
        MeshBuilder.add_box(
            bm,
            size=(platen_w + 0.024, 0.012, platen_h + 0.024),
            offset=(0.0, front_y + 0.006, platen_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Tempered dark glass scan surface
        MeshBuilder.add_box(
            bm,
            size=(platen_w, 0.008, platen_h),
            offset=(0.0, front_y + 0.012, platen_z),
            mat_idx=metal_mat,
            rgba=(0.10, 0.15, 0.18, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
        )

        # Active glowing laser scan line slit
        MeshBuilder.add_box(
            bm,
            size=(platen_w * 0.92, 0.006, 0.01),
            offset=(0.0, front_y + 0.016, platen_z),
            mat_idx=accent_mat,
            rgba=laser_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # Side hand alignment guide rails
        for sx in (-platen_w * 0.5 - 0.008, platen_w * 0.5 + 0.008):
            MeshBuilder.add_box(
                bm,
                size=(0.008, 0.016, platen_h),
                offset=(sx, front_y + 0.012, platen_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )

        # -------------------------------------------------------------
        # 3. Upper Optical Visor / Face Recognition Hood
        # -------------------------------------------------------------
        upper_z = head_z + (half_h * 0.55)

        # Angled brow visor hood
        MeshBuilder.add_box(
            bm,
            size=(w - 0.02, 0.03, 0.08),
            offset=(0.0, front_y + 0.015, upper_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        if self.config.has_face_reticle:
            # Camera aperture cylinder
            MeshBuilder.add_cylinder(
                bm,
                radius=0.024,
                depth=0.018,
                segments=7,
                offset=(0.0, front_y + 0.032, upper_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.06, 0.06, 0.08, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )
            # Internal retina laser indicator diode
            MeshBuilder.add_cylinder(
                bm,
                radius=0.008,
                depth=0.008,
                segments=5,
                offset=(0.0, front_y + 0.040, upper_z),
                axis='Y',
                mat_idx=accent_mat,
                rgba=laser_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # Intercom speaker/mic grill louvers
        if self.config.has_intercom_mic:
            MeshBuilder.add_box(
                bm,
                size=(0.07, 0.006, 0.018),
                offset=(0.0, front_y + 0.003, upper_z - 0.055),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_vent_grate")
            )

        # -------------------------------------------------------------
        # 4. Mount Support (Pedestal or Wall Backplate)
        # -------------------------------------------------------------
        if is_pedestal:
            # Square tubular unistrut stand down to floor
            post_w = 0.08
            post_d = 0.08
            post_h = head_z - (half_h * 0.8)
            MeshBuilder.add_box(
                bm,
                size=(post_w, post_d, post_h),
                offset=(0.0, d * 0.5, post_h * 0.5),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Floor mounting flange plate
            flange_size = 0.22
            MeshBuilder.add_box(
                bm,
                size=(flange_size, flange_size, 0.018),
                offset=(0.0, d * 0.5, 0.009),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Floor anchor bolts
            for bx in (-0.08, 0.08):
                for by in (-0.08, 0.08):
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=0.01,
                        depth=0.02,
                        segments=5,
                        offset=(bx, (d * 0.5) + by, 0.02),
                        axis='Z',
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
        else:
            # Wall mounting base plate
            MeshBuilder.add_box(
                bm,
                size=(w + 0.03, 0.012, h + 0.03),
                offset=(0.0, 0.006, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
