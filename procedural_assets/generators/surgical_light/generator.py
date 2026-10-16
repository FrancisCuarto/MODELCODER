import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SurgicalLightConfig

class SurgicalLightGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for articulated surgical theatre multi-reflector lamps.
    Features ceiling mount flange, counterbalanced pantograph arm, multi-lens satellite
    reflector dish, sterile positioning handle, and perimeter rim grips.
    """

    def generate(self, config: SurgicalLightConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = SurgicalLightConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        dish_radius = self.config.dish_diameter * 0.5
        is_ceiling = (self.config.mount_type == "ceiling")

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)
        lens_rgba = (0.85, 0.95, 1.0, 1.0) if self.config.is_light_on else (0.4, 0.5, 0.55, 0.8)

        mount_top_z = 2.4 if is_ceiling else 1.8

        # -------------------------------------------------------------
        # 1. Mount Flange & Drop Post
        # -------------------------------------------------------------
        if is_ceiling:
            MeshBuilder.add_cylinder(
                bm,
                radius=0.18,
                depth=0.06,
                segments=8,
                offset=(0.0, 0.0, mount_top_z - 0.03),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            rod_len = 0.35
            MeshBuilder.add_cylinder(
                bm,
                radius=0.04,
                depth=rod_len,
                segments=6,
                offset=(0.0, 0.0, mount_top_z - 0.06 - rod_len * 0.5),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            pivot_origin = Vector((0.0, 0.0, mount_top_z - 0.06 - rod_len))
        else:
            MeshBuilder.add_box(
                bm,
                size=(0.25, 0.08, 0.35),
                offset=(0.0, 0.0, mount_top_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            pivot_origin = Vector((0.0, 0.15, mount_top_z))

        # Swivel Hub Block
        MeshBuilder.add_cylinder(
            bm,
            radius=0.07,
            depth=0.12,
            segments=6,
            offset=pivot_origin,
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Articulating Suspension Arm & Counterweight
        # -------------------------------------------------------------
        arm_len = self.config.arm_reach * 0.55
        arm_pitch_rad = math.radians(self.config.arm_pitch_deg)

        arm1_dir = Vector((0.0, math.cos(arm_pitch_rad), math.sin(arm_pitch_rad))).normalized()
        arm1_mid = pivot_origin + arm1_dir * (arm_len * 0.5)

        MeshBuilder.add_box(
            bm,
            size=(0.05, arm_len, 0.05),
            offset=arm1_mid,
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Counterbalance weight
        cb_pos = pivot_origin - arm1_dir * 0.22
        MeshBuilder.add_cylinder(
            bm,
            radius=0.08,
            depth=0.16,
            segments=6,
            offset=cb_pos,
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Elbow Joint
        elbow_pos = pivot_origin + arm1_dir * arm_len
        MeshBuilder.add_cylinder(
            bm,
            radius=0.06,
            depth=0.10,
            segments=6,
            offset=elbow_pos,
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Forearm segment
        forearm_len = self.config.arm_reach * 0.50
        forearm_dir = Vector((0.0, math.cos(arm_pitch_rad - 0.4), math.sin(arm_pitch_rad - 0.4))).normalized()
        forearm_mid = elbow_pos + forearm_dir * (forearm_len * 0.5)

        MeshBuilder.add_box(
            bm,
            size=(0.045, forearm_len, 0.045),
            offset=forearm_mid,
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Gimbal Yoke
        lamp_mount_pos = elbow_pos + forearm_dir * forearm_len
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.10, 0.08),
            offset=lamp_mount_pos,
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Multi-Reflector Satellite Dish
        # -------------------------------------------------------------
        dish_center = lamp_mount_pos + Vector((0.0, 0.08, -0.15))
        dish_th = 0.10

        # Satellite dome back
        MeshBuilder.add_cylinder(
            bm,
            radius=dish_radius,
            depth=dish_th,
            segments=8,
            offset=dish_center - Vector((0.0, 0.0, dish_th * 0.5)),
            axis='Z',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Front recessed bezel plate
        MeshBuilder.add_cylinder(
            bm,
            radius=dish_radius * 0.94,
            depth=0.02,
            segments=8,
            offset=dish_center - Vector((0.0, 0.0, dish_th + 0.005)),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 4. Faceted Reflector Lenses
        # -------------------------------------------------------------
        refl_count = max(3, min(self.config.reflector_count, 6))
        refl_ring_r = dish_radius * 0.55
        refl_lens_r = dish_radius * 0.22
        lens_uv = "fluorescent_lit" if self.config.is_light_on else "glass_reinforced"

        for i in range(refl_count):
            theta = (2.0 * math.pi * i) / refl_count
            lx = math.cos(theta) * refl_ring_r
            ly = math.sin(theta) * refl_ring_r

            lens_pos = dish_center + Vector((lx, ly, -dish_th - 0.015))
            MeshBuilder.add_cylinder(
                bm,
                radius=refl_lens_r,
                depth=0.025,
                segments=6,
                offset=lens_pos,
                axis='Z',
                mat_idx=screen_mat,
                rgba=lens_rgba,
                uv_rect=PS1TextureAtlas.get_rect(lens_uv)
            )

        # -------------------------------------------------------------
        # 5. Central Sterile Handle & Perimeter Grips
        # -------------------------------------------------------------
        if self.config.has_central_handle:
            MeshBuilder.add_cylinder(
                bm,
                radius=0.045,
                depth=0.03,
                segments=6,
                offset=dish_center - Vector((0.0, 0.0, dish_th + 0.02)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            MeshBuilder.add_cylinder(
                bm,
                radius=0.02,
                depth=0.16,
                segments=6,
                offset=dish_center - Vector((0.0, 0.0, dish_th + 0.10)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )
            MeshBuilder.add_cylinder(
                bm,
                radius=0.03,
                depth=0.04,
                segments=6,
                offset=dish_center - Vector((0.0, 0.0, dish_th + 0.18)),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # Perimeter grips
        for rim_side in (-1.0, 1.0):
            MeshBuilder.add_box(
                bm,
                size=(0.025, 0.14, 0.025),
                offset=dish_center + Vector((rim_side * (dish_radius + 0.03), 0.0, -dish_th * 0.5)),
                mat_idx=metal_mat,
                rgba=rubber_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
