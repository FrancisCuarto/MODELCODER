import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SpeakerIntercomConfig

class SpeakerIntercomGenerator(BaseAssetGenerator):
    """
    Procedural generator for wall-mounted two-way technical intercoms.
    Builds cast vandal-resistant box, perforated speaker audio grille, electret microphone,
    prominent mushroom push-to-talk button, and sector identification plate.
    """

    def generate(self, config: SpeakerIntercomConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = SpeakerIntercomConfig()

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

        status_colors = {
            "online": (0.15, 0.95, 0.20, 1.0),
            "calling": (0.95, 0.75, 0.15, 1.0),
            "muted": (0.95, 0.15, 0.15, 1.0),
            "dead": (0.18, 0.18, 0.20, 1.0)
        }
        led_rgba = status_colors.get(self.config.status_light, status_colors["online"])

        w = 0.18
        h = 0.26
        d = 0.06
        half_w = w * 0.5
        half_h = h * 0.5

        # -------------------------------------------------------------
        # 1. Main Cast Aluminum Wall Enclosure
        # -------------------------------------------------------------
        # Base plate with perimeter rim against Y=0
        MeshBuilder.add_box(
            bm,
            size=(w + 0.02, 0.012, h + 0.02),
            offset=(0.0, 0.006, 0.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Front housing block
        MeshBuilder.add_box(
            bm,
            size=(w, d, h),
            offset=(0.0, 0.012 + (d * 0.5), 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        front_y = 0.012 + d

        # -------------------------------------------------------------
        # 2. Speaker Acoustic Grille (Upper portion)
        # -------------------------------------------------------------
        if self.config.has_call_speaker:
            grille_r = 0.048
            grille_z = 0.045
            # Circular outer protective bevel bezel
            MeshBuilder.add_cylinder(
                bm,
                radius=grille_r + 0.008,
                depth=0.01,
                segments=8,
                offset=(0.0, front_y + 0.005, grille_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Internal perforated metal mesh disc
            MeshBuilder.add_cylinder(
                bm,
                radius=grille_r,
                depth=0.006,
                segments=8,
                offset=(0.0, front_y + 0.009, grille_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.12, 0.12, 0.14, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # -------------------------------------------------------------
        # 3. Push-To-Talk (PTT) Button & Microphone (Lower portion)
        # -------------------------------------------------------------
        btn_z = -0.055
        if self.config.has_push_to_talk:
            # Collar surround
            MeshBuilder.add_cylinder(
                bm,
                radius=0.026,
                depth=0.012,
                segments=7,
                offset=(-0.035, front_y + 0.006, btn_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Red mushroom actuator dome
            MeshBuilder.add_cylinder(
                bm,
                radius=0.020,
                depth=0.016,
                segments=7,
                offset=(-0.035, front_y + 0.014, btn_z),
                axis='Y',
                mat_idx=accent_mat,
                rgba=(0.90, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # Electret microphone inlet capsule
        MeshBuilder.add_cylinder(
            bm,
            radius=0.010,
            depth=0.008,
            segments=5,
            offset=(0.038, front_y + 0.004, btn_z),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        # -------------------------------------------------------------
        # 4. Status Indicator LED
        # -------------------------------------------------------------
        MeshBuilder.add_cylinder(
            bm,
            radius=0.007,
            depth=0.010,
            segments=5,
            offset=(0.055, front_y + 0.005, half_h - 0.025),
            axis='Y',
            mat_idx=accent_mat,
            rgba=led_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # -------------------------------------------------------------
        # 5. Stamped Sector Station Label
        # -------------------------------------------------------------
        if self.config.has_station_label:
            MeshBuilder.add_box(
                bm,
                size=(w * 0.55, 0.004, 0.020),
                offset=(-0.015, front_y + 0.002, half_h - 0.025),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 6. Corner Hex Security Screws
        # -------------------------------------------------------------
        screw_x = half_w - 0.012
        screw_z = half_h - 0.012
        for cx in (-screw_x, screw_x):
            for cz in (-screw_z, screw_z):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.006,
                    depth=0.008,
                    segments=5,
                    offset=(cx, front_y + 0.002, cz),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
