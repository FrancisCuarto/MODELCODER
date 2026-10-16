import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CrewShowerConfig

class CrewShowerGenerator(BaseAssetGenerator):
    """
    Procedural generator for crew habitation sanitation shower cubicles.
    Builds non-slip shower receptor tray, central drain, corner sanitary wall paneling,
    overhead spray rose, thermostatic mixer, stainless grab rail, and suspended curtain.
    """

    def generate(self, config: CrewShowerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CrewShowerConfig()

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
        curtain_rgba = (0.78, 0.82, 0.85, 1.0)

        w = max(0.75, self.config.width)
        d = max(0.75, self.config.depth)
        h = max(1.80, self.config.height)

        half_w = w * 0.5
        half_d = d * 0.5

        # -------------------------------------------------------------
        # 1. Floor Shower Receptor Tray & Drain
        # -------------------------------------------------------------
        tray_h = 0.08
        # Outer tray curb
        MeshBuilder.add_box(
            bm,
            size=(w, d, tray_h),
            offset=(0.0, 0.0, tray_h * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Inner textured non-slip floor pan
        MeshBuilder.add_box(
            bm,
            size=(w - 0.08, d - 0.08, 0.02),
            offset=(0.0, 0.0, tray_h - 0.005),
            mat_idx=metal_mat,
            rgba=(0.88, 0.90, 0.92, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )
        # Center circular waste drain
        MeshBuilder.add_cylinder(
            bm,
            radius=0.045,
            depth=0.015,
            segments=7,
            offset=(0.0, 0.0, tray_h + 0.002),
            axis='Z',
            mat_idx=metal_mat,
            rgba=(0.14, 0.14, 0.16, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Corner Enclosure Walls (Back wall at -Y and Left wall at -X)
        # -------------------------------------------------------------
        wall_h = h - tray_h
        wall_t = 0.03
        wall_mid_z = tray_h + (wall_h * 0.5)

        # Back sanitary wall panel
        MeshBuilder.add_box(
            bm,
            size=(w, wall_t, wall_h),
            offset=(0.0, -half_d + (wall_t * 0.5), wall_mid_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Left sanitary wall panel
        MeshBuilder.add_box(
            bm,
            size=(wall_t, d - wall_t, wall_h),
            offset=(-half_w + (wall_t * 0.5), (wall_t * 0.5), wall_mid_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        back_wall_y = -half_d + wall_t

        # -------------------------------------------------------------
        # 3. Plumbing Riser, Mixer & Overhead Rose
        # -------------------------------------------------------------
        # Vertical supply riser pipe along back wall
        MeshBuilder.add_cylinder(
            bm,
            radius=0.014,
            depth=wall_h * 0.75,
            segments=6,
            offset=(0.0, back_wall_y + 0.025, tray_h + (wall_h * 0.45)),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Thermostatic mixer valve block
        mixer_z = tray_h + 1.05
        MeshBuilder.add_box(
            bm,
            size=(0.16, 0.06, 0.08),
            offset=(0.0, back_wall_y + 0.04, mixer_z),
            mat_idx=metal_mat,
            rgba=(0.88, 0.88, 0.92, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Temperature control lever
        MeshBuilder.add_box(
            bm,
            size=(0.02, 0.04, 0.06),
            offset=(0.04, back_wall_y + 0.075, mixer_z),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # Arched overhead shower arm & spray rose
        rose_z = h - 0.15
        MeshBuilder.add_cylinder(
            bm,
            radius=0.014,
            depth=0.28,
            segments=6,
            offset=(0.0, back_wall_y + 0.16, rose_z),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Downward angled shower rose bell
        MeshBuilder.add_cylinder(
            bm,
            radius=0.065,
            depth=0.035,
            segments=7,
            offset=(0.0, back_wall_y + 0.28, rose_z - 0.03),
            axis='Z',
            mat_idx=metal_mat,
            rgba=(0.88, 0.88, 0.92, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 4. Stainless Grab Rail
        # -------------------------------------------------------------
        if self.config.has_grab_rail:
            rail_z = tray_h + 0.85
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=w * 0.55,
                segments=6,
                offset=(0.0, back_wall_y + 0.045, rail_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 5. Curtain Rod & Suspended Curtain
        # -------------------------------------------------------------
        if self.config.has_curtain:
            rod_z = h - 0.06
            rod_y = half_d - 0.04
            # Overhead straight rail bar
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=w,
                segments=6,
                offset=(0.0, rod_y, rod_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Hanging curtain sheet (pleated / gathered on one side)
            curtain_w = w * 0.42
            curtain_h = h - tray_h - 0.12
            curtain_mid_z = tray_h + (curtain_h * 0.5)
            MeshBuilder.add_box(
                bm,
                size=(curtain_w, 0.035, curtain_h),
                offset=(half_w - (curtain_w * 0.5), rod_y, curtain_mid_z),
                mat_idx=accent_mat,
                rgba=curtain_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
