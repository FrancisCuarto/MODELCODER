import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import PressureIndicatorConfig

class PressureIndicatorGenerator(BaseAssetGenerator[PressureIndicatorConfig]):
    """
    Procedural generator for Pressure Indicator:
    Large mural analog dial gauge with rotating needle, cast bezel rim,
    warning sectors, and conduit sensor connection.
    """

    def generate(self, config: PressureIndicatorConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        uv_layer = MeshBuilder.get_or_create_uv_layer(bm)
        col_layer = MeshBuilder.get_or_create_color_layer(bm)

        rad = self.config.diameter / 2.0
        depth = self.config.depth

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        pipe_mat = m_idx.get("pipe", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        glass_rgba = (0.35, 0.65, 0.75, 0.7)

        # 1. Main wall-mount cylindrical bucket
        MeshBuilder.add_cylinder(
            bm,
            radius=rad,
            depth=depth,
            segments=8,
            offset=(0.0, depth / 2.0, rad),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Front outer bezel rim (raised flange)
        MeshBuilder.add_cylinder(
            bm,
            radius=rad * 1.05,
            depth=0.02,
            segments=8,
            offset=(0.0, depth + 0.01, rad),
            axis='Y',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Hex bolts on rim (4 cardinal bolts)
        for i in range(4):
            ang = i * (math.pi / 2.0) + (math.pi / 4.0)
            bx = math.cos(ang) * (rad * 0.96)
            bz = rad + math.sin(ang) * (rad * 0.96)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.012,
                depth=0.015,
                segments=4,
                offset=(bx, depth + 0.02, bz),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.75, 0.75, 0.8, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # 2. Recessed dial face
        dial_rad = rad * 0.88
        MeshBuilder.add_cylinder(
            bm,
            radius=dial_rad,
            depth=0.005,
            segments=8,
            offset=(0.0, depth + 0.003, rad),
            axis='Y',
            mat_idx=screen_mat,
            rgba=(0.95, 0.95, 0.95, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
        )

        # 3. Rotating 3D Needle
        needle_rot = math.radians(self.config.needle_angle)
        needle_len = dial_rad * 0.78
        needle_w = 0.018
        needle_t = 0.006

        rot_mat = mathutils.Euler((0.0, -needle_rot, 0.0), 'XYZ').to_matrix()

        needle_geom = bmesh.ops.create_cube(bm, size=1.0)
        n_verts = [v for v in needle_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in n_verts:
            v.co.x *= needle_w
            v.co.y *= needle_t
            v.co.z *= needle_len
            # Pivot around bottom
            v.co.z += needle_len / 2.0
            v.co = rot_mat @ v.co
            v.co.y += depth + 0.01
            v.co.z += rad

        for f in bm.faces:
            if all(v in n_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, screen_mat, (0.85, 0.15, 0.12, 1.0), col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("button_red"))

        # Central needle spindle cap
        MeshBuilder.add_cylinder(
            bm,
            radius=0.025,
            depth=0.012,
            segments=6,
            offset=(0.0, depth + 0.012, rad),
            axis='Y',
            mat_idx=metal_mat,
            rgba=(0.15, 0.15, 0.18, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 4. Protective lens glass
        if self.config.has_protective_glass:
            MeshBuilder.add_cylinder(
                bm,
                radius=dial_rad * 0.98,
                depth=0.004,
                segments=8,
                offset=(0.0, depth + 0.018, rad),
                axis='Y',
                mat_idx=glass_mat,
                rgba=glass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )


        # 5. Bottom sensor conduit fitting
        if self.config.has_bottom_pipe_fitting:
            MeshBuilder.add_cylinder(
                bm,
                radius=0.03,
                depth=0.08,
                segments=6,
                offset=(0.0, depth * 0.5, -0.04),
                axis='Z',
                mat_idx=pipe_mat,
                rgba=(0.35, 0.4, 0.45, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Sector placard plate
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.006, 0.05),
            offset=(0.0, depth + 0.015, rad * 2.0 + 0.01),
            mat_idx=screen_mat,
            rgba=(0.2, 0.5, 0.8, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("sign_sector_blue")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
