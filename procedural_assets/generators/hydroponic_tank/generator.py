import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import HydroponicTankConfig

class HydroponicTankGenerator(BaseAssetGenerator):
    """
    Procedural generator for botanical hydroponic nutrient solution reservoir tanks.
    Builds elevated steel cradle legs, cylindrical pressurized vessel, calibrated sight glass tube,
    fluid fill/drain manifold pipes, and pressure relief valve wheel.
    """

    def generate(self, config: HydroponicTankConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = HydroponicTankConfig()

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

        solution_colors = {
            "nutrient_rich": (0.20, 0.85, 0.35, 1.0),
            "low_reserve": (0.95, 0.65, 0.15, 1.0),
            "algae_bloom": (0.25, 0.50, 0.18, 1.0)
        }
        liquid_rgba = solution_colors.get(self.config.solution_type, solution_colors["nutrient_rich"])

        h = max(0.8, self.config.tank_height)
        r = max(0.25, self.config.tank_radius)
        leg_h = 0.18
        tank_z = leg_h + (h * 0.5)

        # -------------------------------------------------------------
        # 1. Base Support Legs & Cradle
        # -------------------------------------------------------------
        # 4 diagonal corner tubular legs
        for lx, ly in ((-r * 0.75, -r * 0.75), (r * 0.75, -r * 0.75), (-r * 0.75, r * 0.75), (r * 0.75, r * 0.75)):
            # Leg tube
            MeshBuilder.add_box(
                bm,
                size=(0.045, 0.045, leg_h + 0.08),
                offset=(lx, ly, (leg_h + 0.08) * 0.5),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Base foot pad
            MeshBuilder.add_box(
                bm,
                size=(0.09, 0.09, 0.015),
                offset=(lx, ly, 0.0075),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )

        # Bottom ring collar
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 1.05,
            depth=0.03,
            segments=8,
            offset=(0.0, 0.0, leg_h),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        # -------------------------------------------------------------
        # 2. Main Cylindrical Tank Body
        # -------------------------------------------------------------
        # Central cylinder
        MeshBuilder.add_cylinder(
            bm,
            radius=r,
            depth=h,
            segments=8,
            offset=(0.0, 0.0, tank_z),
            axis='Z',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Top dome cap
        top_z = leg_h + h
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 0.95,
            depth=0.06,
            segments=8,
            offset=(0.0, 0.0, top_z + 0.03),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        # -------------------------------------------------------------
        # 3. Sight Glass Liquid Level Tube
        # -------------------------------------------------------------
        if self.config.has_sight_glass:
            sight_h = h * 0.72
            sight_y = r + 0.02
            sight_mid_z = leg_h + (h * 0.5)

            # Top & bottom 90-deg brass elbow fittings
            for bz in (sight_mid_z - (sight_h * 0.5), sight_mid_z + (sight_h * 0.5)):
                MeshBuilder.add_box(
                    bm,
                    size=(0.03, 0.04, 0.03),
                    offset=(0.0, sight_y, bz),
                    mat_idx=metal_mat,
                    rgba=(0.85, 0.75, 0.25, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

            # Outer transparent acrylic gauge column
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=sight_h,
                segments=6,
                offset=(0.0, sight_y + 0.01, sight_mid_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.85, 0.90, 0.92, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Inner glowing liquid column indicating level
            lvl = max(0.05, min(1.0, self.config.liquid_level))
            liq_h = sight_h * lvl
            liq_mid_z = (sight_mid_z - (sight_h * 0.5)) + (liq_h * 0.5)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.011,
                depth=liq_h,
                segments=6,
                offset=(0.0, sight_y + 0.01, liq_mid_z),
                axis='Z',
                mat_idx=accent_mat,
                rgba=liquid_rgba,
                uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
            )

        # -------------------------------------------------------------
        # 4. Feed/Drain Pipes & Valve Wheel
        # -------------------------------------------------------------
        if self.config.has_feed_pipes:
            # Top fill pipe and valve
            MeshBuilder.add_cylinder(
                bm,
                radius=0.028,
                depth=0.12,
                segments=6,
                offset=(0.0, 0.0, top_z + 0.12),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Red handwheel valve
            MeshBuilder.add_cylinder(
                bm,
                radius=0.07,
                depth=0.018,
                segments=7,
                offset=(0.0, 0.0, top_z + 0.19),
                axis='Z',
                mat_idx=accent_mat,
                rgba=(0.90, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            # Side discharge drain manifold
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=0.10,
                segments=6,
                offset=(r + 0.05, 0.0, leg_h + 0.10),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
