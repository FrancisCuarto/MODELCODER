import bpy
import bmesh
import math
from mathutils import Vector, Matrix
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import AntennaDishConfig

class AntennaDishGenerator(BaseAssetGenerator):
    """
    Procedural generator for directional parabolic communications antenna dishes.
    Builds pedestal or wall gimbal mount, azimuth/elevation yoke, concave faceted dish,
    rear structural ribbing, and focal sub-reflector feedhorn.
    """

    def generate(self, config: AntennaDishConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = AntennaDishConfig()

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
        yellow_rgba = (0.95, 0.85, 0.20, 1.0)

        dia = max(0.5, self.config.dish_diameter)
        radius = dia * 0.5
        depth = max(0.10, self.config.dish_depth)

        # -------------------------------------------------------------
        # 1. Base Mounting (Pedestal or Wall Bracket)
        # -------------------------------------------------------------
        if self.config.mount_type == "wall_bracket":
            pivot_center = Vector((0.0, 0.35, 0.0))
            # Wall backplate at Y=0
            MeshBuilder.add_box(
                bm,
                size=(0.28, 0.02, 0.28),
                offset=(0.0, 0.01, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Cantilever extension pipe
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=0.35,
                segments=6,
                offset=(0.0, 0.175, 0.0),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        else:
            pivot_center = Vector((0.0, 0.0, 0.45))
            # Circular floor flange
            MeshBuilder.add_cylinder(
                bm,
                radius=0.22,
                depth=0.02,
                segments=8,
                offset=(0.0, 0.0, 0.01),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Vertical pedestal pillar
            MeshBuilder.add_cylinder(
                bm,
                radius=0.045,
                depth=0.43,
                segments=6,
                offset=(0.0, 0.0, 0.235),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Azimuth rotor head cylinder
        MeshBuilder.add_cylinder(
            bm,
            radius=0.065,
            depth=0.08,
            segments=7,
            offset=tuple(pivot_center),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Steerable Dish & Feedhorn Sub-Assembly
        # -------------------------------------------------------------
        azi_rad = math.radians(self.config.azimuth_angle)
        ele_rad = math.radians(self.config.elevation_angle)
        rot_mat = Matrix.Rotation(azi_rad, 4, 'Z') @ Matrix.Rotation(-ele_rad, 4, 'X')

        dish_faces = []

        # Rear mounting hub cylinder
        hub = MeshBuilder.add_cylinder(
            bm,
            radius=radius * 0.35,
            depth=0.08,
            segments=8,
            offset=(0.0, -0.04, 0.0),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        dish_faces.extend(hub)

        # Main parabolic dish outer rim and concave body
        dish_rim = MeshBuilder.add_cylinder(
            bm,
            radius=radius,
            depth=depth,
            segments=8,
            offset=(0.0, depth * 0.5, 0.0),
            axis='Y',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        dish_faces.extend(dish_rim)

        # Inner reflector cone inset
        inner_cone = MeshBuilder.add_cylinder(
            bm,
            radius=radius * 0.88,
            depth=depth * 0.85,
            segments=8,
            offset=(0.0, depth * 0.55, 0.0),
            axis='Y',
            mat_idx=metal_mat,
            rgba=(0.88, 0.88, 0.92, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        dish_faces.extend(inner_cone)

        # -------------------------------------------------------------
        # 3. Feedhorn & Focal Struts
        # -------------------------------------------------------------
        if self.config.has_sub_reflector:
            focal_dist = depth + (radius * 0.65)
            # 3 tripod struts reaching from dish rim to focal head
            for si in range(3):
                sang = si * (math.pi * 2.0 / 3.0)
                rim_x = math.cos(sang) * (radius * 0.85)
                rim_z = math.sin(sang) * (radius * 0.85)
                strut_mid_x = rim_x * 0.5
                strut_mid_z = rim_z * 0.5
                strut_mid_y = focal_dist * 0.5

                strut = MeshBuilder.add_box(
                    bm,
                    size=(0.015, focal_dist * 0.9, 0.015),
                    offset=(strut_mid_x, strut_mid_y, strut_mid_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                dish_faces.extend(strut)

            # Central focal feedhorn sensor cylinder
            feed = MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=0.06,
                segments=6,
                offset=(0.0, focal_dist, 0.0),
                axis='Y',
                mat_idx=accent_mat,
                rgba=yellow_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            dish_faces.extend(feed)

        # Apply Azimuth/Elevation rotation around pivot_center
        dish_verts = list({v for f in dish_faces for v in f.verts})
        trans_mat = Matrix.Translation(pivot_center)
        bmesh.ops.transform(bm, matrix=trans_mat @ rot_mat, verts=dish_verts)

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
