import math
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import OxygenTankConfig

class OxygenTankGenerator(BaseAssetGenerator[OxygenTankConfig]):
    """
    Procedural generator for Oxygen Tank:
    Faceted high-pressure industrial gas canister with roll-cage valve protector,
    foot ring, shoulder gauge, and hazard markings.
    """

    def generate(self, config: OxygenTankConfig = None) -> bpy.types.Object:
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

        r = self.config.tank_radius
        h = self.config.tank_height

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        brass_rgba = (0.85, 0.68, 0.22, 1.0)

        # Body color & texture selection
        if self.config.tank_color == "cyan":
            tank_rect = PS1TextureAtlas.get_rect("oxygen_cyan_glow")
            tank_rgba = (0.2, 0.75, 0.85, 1.0)
        elif self.config.tank_color == "white":
            tank_rect = PS1TextureAtlas.get_rect("painted_metal_white")
            tank_rgba = (0.9, 0.92, 0.94, 1.0)
        else:
            tank_rect = PS1TextureAtlas.get_rect("hazard_stripes")
            tank_rgba = (0.9, 0.75, 0.15, 1.0)

        # 1. Base foot ring
        foot_h = 0.08
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 1.05,
            depth=foot_h,
            segments=8,
            offset=(0.0, 0.0, foot_h / 2.0),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 2. Main cylindrical tank body
        body_h = h - foot_h - 0.25
        body_z = foot_h + body_h / 2.0
        MeshBuilder.add_cylinder(
            bm,
            radius=r,
            depth=body_h,
            segments=8,
            offset=(0.0, 0.0, body_z),
            axis='Z',
            mat_idx=casing_mat,
            rgba=tank_rgba,
            uv_rect=tank_rect
        )

        # 3. Tapered domed shoulder
        shoulder_h = 0.14
        shoulder_z = foot_h + body_h + shoulder_h / 2.0
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 0.75,
            depth=shoulder_h,
            segments=8,
            offset=(0.0, 0.0, shoulder_z),
            axis='Z',
            mat_idx=casing_mat,
            rgba=tank_rgba,
            uv_rect=tank_rect
        )

        # Hazard collar band
        if self.config.has_hazard_collar:
            collar_h = 0.06
            MeshBuilder.add_cylinder(
                bm,
                radius=r * 1.02,
                depth=collar_h,
                segments=8,
                offset=(0.0, 0.0, foot_h + body_h - collar_h / 2.0),
                axis='Z',
                mat_idx=screen_mat,
                rgba=(0.95, 0.8, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # 4. Top brass neck & valve
        neck_h = 0.10
        neck_z = foot_h + body_h + shoulder_h + neck_h / 2.0
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 0.32,
            depth=neck_h,
            segments=6,
            offset=(0.0, 0.0, neck_z),
            axis='Z',
            mat_idx=brass_mat,
            rgba=brass_rgba,
            uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
        )

        # Cross valve handwheel on top
        MeshBuilder.add_cylinder(
            bm,
            radius=r * 0.40,
            depth=0.03,
            segments=6,
            offset=(0.0, 0.0, neck_z + neck_h / 2.0 + 0.015),
            axis='Z',
            mat_idx=metal_mat,
            rgba=(0.85, 0.15, 0.12, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("button_red")
        )

        # Threaded outlet nozzle
        MeshBuilder.add_cylinder(
            bm,
            radius=0.02,
            depth=0.06,
            segments=6,
            offset=(0.0, r * 0.35, neck_z),
            axis='Y',
            mat_idx=brass_mat,
            rgba=brass_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # 5. Shoulder mini gauge
        if self.config.has_mini_gauge:
            gauge_rad = 0.035
            MeshBuilder.add_cylinder(
                bm,
                radius=gauge_rad,
                depth=0.025,
                segments=8,
                offset=(0.0, -r * 0.85, shoulder_z + 0.02),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

        # 6. Protective tubular roll-cage collar handle
        if self.config.has_top_handle_cage:
            cage_rad = r * 0.80
            cage_top_z = neck_z + neck_h / 2.0 + 0.06
            # Tubular top ring
            MeshBuilder.add_cylinder(
                bm,
                radius=cage_rad,
                depth=0.025,
                segments=8,
                offset=(0.0, 0.0, cage_top_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # 3 vertical support struts
            for i in range(3):
                ang = i * (2.0 * math.pi / 3.0)
                sx = math.cos(ang) * (cage_rad * 0.9)
                sy = math.sin(ang) * (cage_rad * 0.9)
                strut_h = cage_top_z - shoulder_z
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.012,
                    depth=strut_h,
                    segments=4,
                    offset=(sx, sy, shoulder_z + strut_h / 2.0),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
