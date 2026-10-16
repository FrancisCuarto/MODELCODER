import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import AirlockChamberConfig

class AirlockChamberGenerator(BaseAssetGenerator[AirlockChamberConfig]):
    """
    Procedural generator for Airlock Chamber:
    Modular decompression transition vault with dual heavy sliding bulkhead doors,
    floor grate, vacuum cycle vents, and EVA emergency grab bars.
    """

    def generate(self, config: AirlockChamberConfig = None) -> bpy.types.Object:
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

        L = self.config.chamber_length
        W = self.config.chamber_width
        H = self.config.chamber_height

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        glass_rgba = (0.35, 0.65, 0.75, 0.85)

        wall_t = 0.15
        floor_h = 0.12

        # 1. Structural base and floor
        MeshBuilder.add_box(
            bm,
            size=(W, L, floor_h),
            offset=(0.0, 0.0, floor_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Walking floor grating
        if self.config.has_floor_grate:
            MeshBuilder.add_box(
                bm,
                size=(W * 0.65, L * 0.88, 0.02),
                offset=(0.0, 0.0, floor_h + 0.01),
                mat_idx=metal_mat,
                rgba=(0.25, 0.25, 0.28, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # 2. Side Walls
        wall_h = H - floor_h - 0.15
        wall_z = floor_h + wall_h / 2.0
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(wall_t, L, wall_h),
                offset=(sx * (W / 2.0 - wall_t / 2.0), 0.0, wall_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # 3. Ceiling roof slab
        roof_h = 0.15
        MeshBuilder.add_box(
            bm,
            size=(W, L, roof_h),
            offset=(0.0, 0.0, H - roof_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Ceiling fluorescent fixture
        MeshBuilder.add_box(
            bm,
            size=(0.4, L * 0.7, 0.06),
            offset=(0.0, 0.0, H - roof_h - 0.03),
            mat_idx=screen_mat,
            rgba=(0.95, 0.95, 0.85, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("fluorescent_lit")
        )

        # 4. Front & Rear Portal Bulkhead Frames
        portal_w = W * 0.7
        portal_h = H * 0.78
        door_w = portal_w * 0.48
        door_h = portal_h * 0.98
        door_t = 0.08

        for end_idx, sy in enumerate((-1, 1)):
            portal_y = sy * (L / 2.0 - wall_t / 2.0)
            
            # Left & right frame jambs
            jamb_w = (W - portal_w) / 2.0
            for sx in (-1, 1):
                MeshBuilder.add_box(
                    bm,
                    size=(jamb_w, wall_t, portal_h),
                    offset=(sx * (W / 2.0 - jamb_w / 2.0), portal_y, floor_h + portal_h / 2.0),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

            # Header lintel with hazard chevrons
            lintel_h = (H - floor_h - portal_h)
            MeshBuilder.add_box(
                bm,
                size=(portal_w, wall_t, lintel_h),
                offset=(0.0, portal_y, floor_h + portal_h + lintel_h / 2.0),
                mat_idx=screen_mat,
                rgba=(0.95, 0.8, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

            # Sliding Door Panels (2 split leaves per portal)
            fraction_open = self.config.inner_door_open if sy < 0 else self.config.outer_door_open
            slide_offset = fraction_open * (door_w * 0.85)

            for leaf_dir in (-1, 1):
                leaf_x = leaf_dir * (door_w / 2.0 + slide_offset)
                MeshBuilder.add_box(
                    bm,
                    size=(door_w, door_t, door_h),
                    offset=(leaf_x, portal_y, floor_h + door_h / 2.0),
                    mat_idx=metal_mat,
                    rgba=(0.4, 0.42, 0.45, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

                # Reinforced circular porthole inspection glass on each leaf
                porthole_rad = 0.14
                porthole_z = floor_h + door_h * 0.65
                MeshBuilder.add_cylinder(
                    bm,
                    radius=porthole_rad,
                    depth=door_t + 0.01,
                    segments=8,
                    offset=(leaf_x, portal_y, porthole_z),
                    axis='Y',
                    mat_idx=glass_mat,
                    rgba=glass_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
                )

        # 5. Side wall atmospheric vent grills
        if self.config.has_depressurize_vents:
            for sx in (-1, 1):
                MeshBuilder.add_box(
                    bm,
                    size=(0.02, L * 0.45, 0.35),
                    offset=(sx * (W / 2.0 - wall_t - 0.01), 0.0, wall_z + 0.25),
                    mat_idx=metal_mat,
                    rgba=(0.2, 0.2, 0.22, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("vent_grill")
                )

        # 6. EVA yellow grab bars along walls
        if self.config.has_eva_grab_bars:
            bar_z = floor_h + 1.05
            for sx in (-1, 1):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.022,
                    depth=L * 0.75,
                    segments=6,
                    offset=(sx * (W / 2.0 - wall_t - 0.06), 0.0, bar_z),
                    axis='Y',
                    mat_idx=screen_mat,
                    rgba=(0.95, 0.8, 0.1, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("button_yellow")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
