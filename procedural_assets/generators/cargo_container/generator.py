import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CargoContainerConfig

class CargoContainerGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for standardized interstellar logistics cargo containers.
    Builds structural ISO corner twistlock castings, corrugated side wall panels,
    forklift tine pocket channels, roof reinforcement ribs, hinged rear cargo doors with vertical cam rods,
    and hazard classification placards.
    """

    def generate(self, config: CargoContainerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CargoContainerConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        l = self.config.container_length
        w = self.config.container_width
        h = self.config.container_height
        half_l = l * 0.5
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")

        # Color based on cargo class
        c_class = self.config.cargo_class
        if c_class == "cryo_hazard":
            body_rgba = (0.20, 0.45, 0.55, 1.0)
            hazard_uv = "oxygen_cyan_glow"
        elif c_class == "armory_munitions":
            body_rgba = (0.50, 0.22, 0.18, 1.0)
            hazard_uv = "hazard_stripes"
        else:
            body_rgba = casing_rgba
            hazard_uv = "caution_label"

        # -------------------------------------------------------------
        # 1. Main Hull Enclosure (Walls, Roof, Floor)
        # -------------------------------------------------------------
        wall_th = 0.04
        # Floor slab
        MeshBuilder.add_box(
            bm,
            size=(w - 0.04, l - 0.04, wall_th),
            offset=(0.0, 0.0, wall_th * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Roof slab
        MeshBuilder.add_box(
            bm,
            size=(w - 0.04, l - 0.04, wall_th),
            offset=(0.0, 0.0, h - wall_th * 0.5),
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Front sealed bulkhead wall (at -half_l)
        MeshBuilder.add_box(
            bm,
            size=(w - 0.04, wall_th, h - wall_th * 2),
            offset=(0.0, -half_l + wall_th * 0.5, h * 0.5),
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Left wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, l - 0.04, h - wall_th * 2),
            offset=(-half_w + wall_th * 0.5, 0.0, h * 0.5),
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Right wall
        MeshBuilder.add_box(
            bm,
            size=(wall_th, l - 0.04, h - wall_th * 2),
            offset=(half_w - wall_th * 0.5, 0.0, h * 0.5),
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # -------------------------------------------------------------
        # 2. Eight Heavy ISO Corner Twistlock Castings
        # -------------------------------------------------------------
        cast_s = 0.12
        for cx in (-half_w + cast_s * 0.5, half_w - cast_s * 0.5):
            for cy in (-half_l + cast_s * 0.5, half_l - cast_s * 0.5):
                for cz in (cast_s * 0.5, h - cast_s * 0.5):
                    # Casting cube block
                    MeshBuilder.add_box(
                        bm,
                        size=(cast_s, cast_s, cast_s),
                        offset=(cx, cy, cz),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        # -------------------------------------------------------------
        # 3. Corrugated Side Wall Reinforcement Ribs
        # -------------------------------------------------------------
        ribs = max(3, min(self.config.corrugation_ribs, 8))
        rib_span = l - cast_s * 2.2
        rib_step = rib_span / (ribs + 1)
        rib_w = 0.025
        rib_d = 0.08
        rib_h = h - cast_s * 1.5

        for ri in range(1, ribs + 1):
            ry = -half_l + cast_s * 1.1 + ri * rib_step
            # Left side rib
            MeshBuilder.add_box(
                bm,
                size=(rib_w, rib_d, rib_h),
                offset=(-half_w - rib_w * 0.5 + 0.01, ry, h * 0.5),
                mat_idx=casing_mat,
                rgba=body_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Right side rib
            MeshBuilder.add_box(
                bm,
                size=(rib_w, rib_d, rib_h),
                offset=(half_w + rib_w * 0.5 - 0.01, ry, h * 0.5),
                mat_idx=casing_mat,
                rgba=body_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # -------------------------------------------------------------
        # 4. Transverse Forklift Pocket Sleeves
        # -------------------------------------------------------------
        if self.config.has_forklift_pockets:
            pocket_w = w * 1.01
            pocket_l = 0.22
            pocket_h = 0.10
            for py in (-half_l * 0.35, half_l * 0.35):
                # Tunnel sleeve
                MeshBuilder.add_box(
                    bm,
                    size=(pocket_w, pocket_l, pocket_h),
                    offset=(0.0, py, pocket_h * 0.5 + 0.01),
                    mat_idx=metal_mat,
                    rgba=(0.12, 0.12, 0.14, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 5. Rear Cargo Access Doors (at +half_l)
        # -------------------------------------------------------------
        door_w = (w - cast_s * 1.8) * 0.5
        door_th = 0.04
        door_h = h - cast_s * 1.8
        door_z = h * 0.5

        angle_deg = max(0.0, min(self.config.doors_open_angle, 85.0))
        angle_rad = math.radians(angle_deg)
        cos_d = math.cos(angle_rad)
        sin_d = math.sin(angle_rad)

        # Left door hinge at (-door_w, half_l - 0.02)
        lh_x = -door_w
        lh_y = half_l - 0.02
        # Right door hinge at (door_w, half_l - 0.02)
        rh_x = door_w
        rh_y = half_l - 0.02

        def rotate_door_left(lx, ly, lz):
            dx = lx - lh_x
            dy = ly - lh_y
            rx = lh_x + dx * cos_d + dy * sin_d
            ry = lh_y - dx * sin_d + dy * cos_d
            return (rx, ry, lz)

        def rotate_door_right(lx, ly, lz):
            dx = lx - rh_x
            dy = ly - rh_y
            rx = rh_x + dx * cos_d - dy * sin_d
            ry = rh_y + dx * sin_d + dy * cos_d
            return (rx, ry, lz)

        # Left Door Slab
        p_ldoor = rotate_door_left(-door_w * 0.5, half_l - door_th * 0.5, door_z)
        MeshBuilder.add_box(
            bm,
            size=(door_w, door_th, door_h),
            offset=p_ldoor,
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Right Door Slab
        p_rdoor = rotate_door_right(door_w * 0.5, half_l - door_th * 0.5, door_z)
        MeshBuilder.add_box(
            bm,
            size=(door_w, door_th, door_h),
            offset=p_rdoor,
            mat_idx=casing_mat,
            rgba=body_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Vertical Locking Cam Rods
        # Left door rod
        p_lrod = rotate_door_left(-door_w * 0.25, half_l + 0.015, door_z)
        MeshBuilder.add_cylinder(
            bm,
            radius=0.016,
            depth=door_h * 0.95,
            segments=5,
            offset=p_lrod,
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Right door rod
        p_rrod = rotate_door_right(door_w * 0.25, half_l + 0.015, door_z)
        MeshBuilder.add_cylinder(
            bm,
            radius=0.016,
            depth=door_h * 0.95,
            segments=5,
            offset=p_rrod,
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 6. Hazard Placards & Stencils
        # -------------------------------------------------------------
        # Side hazard diamond plaque
        MeshBuilder.add_box(
            bm,
            size=(0.02, 0.24, 0.24),
            offset=(-half_w - 0.015, 0.0, h * 0.65),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect(hazard_uv)
        )
        MeshBuilder.add_box(
            bm,
            size=(0.02, 0.24, 0.24),
            offset=(half_w + 0.015, 0.0, h * 0.65),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect(hazard_uv)
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
