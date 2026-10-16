import math
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import OxygenRegulatorConfig

class OxygenRegulatorGenerator(BaseAssetGenerator[OxygenRegulatorConfig]):
    """
    Procedural generator for Oxygen Regulator:
    Mural pressure reduction manifold with dual analog Bourdon gauges,
    brass needle valves, and high-pressure supply line fittings.
    """

    def generate(self, config: OxygenRegulatorConfig = None) -> bpy.types.Object:
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

        w = self.config.width
        h = self.config.height

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        pipe_mat = m_idx.get("pipe", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        brass_rgba = (0.85, 0.68, 0.22, 1.0)

        # 1. Wall backplate
        plate_t = 0.02
        MeshBuilder.add_box(
            bm,
            size=(w, plate_t, h),
            offset=(0.0, -plate_t / 2.0, h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Corner mounting bolts
        for sx in (-1, 1):
            for sz in (-1, 1):
                bx = sx * (w / 2.0 - 0.04)
                bz = h / 2.0 + sz * (h / 2.0 - 0.04)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.015,
                    depth=0.015,
                    segments=6,
                    offset=(bx, 0.008, bz),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=(0.7, 0.7, 0.75, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # Stamped caution label on backplate
        MeshBuilder.add_box(
            bm,
            size=(0.14, 0.005, 0.06),
            offset=(0.0, 0.003, h * 0.82),
            mat_idx=screen_mat,
            rgba=(0.95, 0.8, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("caution_label")
        )

        # 2. Central brass manifold block
        mani_w = w * 0.65
        mani_h = 0.12
        mani_d = 0.12
        mani_z = h * 0.42
        MeshBuilder.add_box(
            bm,
            size=(mani_w, mani_d, mani_h),
            offset=(0.0, mani_d / 2.0, mani_z),
            mat_idx=brass_mat,
            rgba=brass_rgba,
            uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
        )

        # 3. Pressure gauges mounted on top of manifold
        num_gauges = max(1, min(3, int(self.config.gauge_count)))
        gauge_rad = 0.075
        gauge_depth = 0.045
        g_spacing = mani_w / float(num_gauges + 1)

        for i in range(num_gauges):
            gx = -mani_w / 2.0 + (i + 1) * g_spacing
            gz = mani_z + mani_h / 2.0 + gauge_rad + 0.02
            gy = mani_d / 2.0 + 0.02

            # Gauge stem
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.04,
                segments=6,
                offset=(gx, gy, mani_z + mani_h / 2.0 + 0.02),
                axis='Z',
                mat_idx=brass_mat,
                rgba=brass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )

            # Circular gauge bezel
            MeshBuilder.add_cylinder(
                bm,
                radius=gauge_rad,
                depth=gauge_depth,
                segments=10,
                offset=(gx, gy, gz),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Dial meter face
            MeshBuilder.add_cylinder(
                bm,
                radius=gauge_rad * 0.85,
                depth=0.005,
                segments=10,
                offset=(gx, gy + gauge_depth / 2.0 + 0.003, gz),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

        # 4. Fluted brass / red control valves
        if self.config.has_brass_valves:
            # Front adjustment knob
            MeshBuilder.add_cylinder(
                bm,
                radius=0.04,
                depth=0.05,
                segments=8,
                offset=(0.0, mani_d + 0.03, mani_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.85, 0.15, 0.12, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        # 5. Flow-meter vertical tube
        if self.config.has_flow_meter:
            flow_x = mani_w / 2.0 + 0.05
            flow_z = mani_z + 0.08
            MeshBuilder.add_cylinder(
                bm,
                radius=0.02,
                depth=0.18,
                segments=6,
                offset=(flow_x, mani_d * 0.6, flow_z),
                axis='Z',
                mat_idx=glass_mat,
                rgba=(0.4, 0.8, 0.9, 0.8),
                uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
            )

        # 6. Inlet and outlet pipe couplings
        # Bottom inlet pipe
        MeshBuilder.add_cylinder(
            bm,
            radius=0.025,
            depth=h * 0.35,
            segments=6,
            offset=(-mani_w * 0.25, mani_d * 0.4, h * 0.18),
            axis='Z',
            mat_idx=pipe_mat,
            rgba=(0.4, 0.45, 0.5, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Top outlet fitting
        MeshBuilder.add_cylinder(
            bm,
            radius=0.022,
            depth=0.12,
            segments=6,
            offset=(mani_w * 0.25, mani_d * 0.4, h * 0.75),
            axis='Z',
            mat_idx=pipe_mat,
            rgba=(0.4, 0.45, 0.5, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 7. Emergency shutoff lever
        if self.config.has_emergency_shutoff:
            lever_x = -mani_w / 2.0 - 0.04
            MeshBuilder.add_box(
                bm,
                size=(0.03, 0.08, 0.03),
                offset=(lever_x, mani_d * 0.5, mani_z),
                mat_idx=metal_mat,
                rgba=(0.9, 0.1, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
