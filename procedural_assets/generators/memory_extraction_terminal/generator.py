import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import MemoryExtractionTerminalConfig

class MemoryExtractionTerminalGenerator(BaseAssetGenerator[MemoryExtractionTerminalConfig]):
    """
    Procedural generator for Memory Extraction Terminal:
    Station operation console with angled CRT, mechanical keyboard, neural cartridge
    reader receptacle, and tape telemetry drive.
    """

    def generate(self, config: MemoryExtractionTerminalConfig = None) -> bpy.types.Object:
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

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")

        # 1. Base / Support
        desk_w = 0.75
        desk_d = 0.55
        if self.config.mount_style == "pedestal":
            pedestal_h = 0.72
            # Floor plate
            MeshBuilder.add_box(
                bm,
                size=(0.55, 0.55, 0.04),
                offset=(0.0, 0.0, 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Heavy column
            MeshBuilder.add_box(
                bm,
                size=(0.24, 0.24, pedestal_h),
                offset=(0.0, -0.05, pedestal_h / 2.0 + 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            shelf_z = pedestal_h + 0.02
        else:
            shelf_z = 0.04
            MeshBuilder.add_box(
                bm,
                size=(desk_w, desk_d, 0.04),
                offset=(0.0, 0.0, 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        # 2. Main slanted console table
        con_h = 0.12
        MeshBuilder.add_box(
            bm,
            size=(desk_w, desk_d, con_h),
            offset=(0.0, 0.0, shelf_z + con_h / 2.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
        )

        # Slanted keyboard area
        MeshBuilder.add_box(
            bm,
            size=(desk_w * 0.52, desk_d * 0.42, 0.03),
            offset=(-desk_w * 0.18, -desk_d * 0.18, shelf_z + con_h + 0.015),
            mat_idx=metal_mat,
            rgba=(0.18, 0.18, 0.20, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # Keyboard keys block
        MeshBuilder.add_box(
            bm,
            size=(desk_w * 0.48, desk_d * 0.36, 0.02),
            offset=(-desk_w * 0.18, -desk_d * 0.18, shelf_z + con_h + 0.03),
            mat_idx=casing_mat,
            rgba=(0.8, 0.8, 0.82, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("button_white")
        )

        # Cartridge reader bay on right side of keyboard
        slot_w = 0.14
        slot_d = 0.22
        MeshBuilder.add_box(
            bm,
            size=(slot_w + 0.04, slot_d + 0.04, 0.05),
            offset=(desk_w * 0.24, -desk_d * 0.15, shelf_z + con_h + 0.025),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        if self.config.cartridge_inserted:
            # Memory cartridge sticking out of reader slot
            MeshBuilder.add_box(
                bm,
                size=(slot_w * 0.85, slot_d * 0.75, 0.06),
                offset=(desk_w * 0.24, -desk_d * 0.12, shelf_z + con_h + 0.05),
                mat_idx=brass_mat,
                rgba=(0.85, 0.65, 0.18, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )
            # Gold edge contacts
            MeshBuilder.add_box(
                bm,
                size=(slot_w * 0.6, 0.03, 0.03),
                offset=(desk_w * 0.24, -desk_d * 0.12 + slot_d * 0.35, shelf_z + con_h + 0.07),
                mat_idx=metal_mat,
                rgba=(0.95, 0.8, 0.2, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )

        # 3. Bulky CRT monitor housing
        crt_w = 0.46
        crt_h = 0.36
        crt_d = 0.38
        crt_base_z = shelf_z + con_h + crt_h / 2.0 + 0.04
        crt_base_y = desk_d * 0.12

        tilt_rad = math.radians(self.config.crt_tilt)
        rot_mat = mathutils.Euler((tilt_rad, 0.0, 0.0), 'XYZ').to_matrix()

        crt_geom = bmesh.ops.create_cube(bm, size=1.0)
        c_verts = [v for v in crt_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in c_verts:
            v.co.x *= crt_w
            v.co.y *= crt_d
            v.co.z *= crt_h
            # Rotate tilt
            v.co = rot_mat @ v.co
            v.co.x += -desk_w * 0.10
            v.co.y += crt_base_y
            v.co.z += crt_base_z

        for f in bm.faces:
            if all(v in c_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, casing_mat, casing_rgba, col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("beige_plastic_worn"))

        # CRT Screen face
        screen_geom = bmesh.ops.create_cube(bm, size=1.0)
        s_verts = [v for v in screen_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in s_verts:
            v.co.x *= crt_w * 0.78
            v.co.y *= 0.02
            v.co.z *= crt_h * 0.74
            v.co = rot_mat @ v.co
            # Offset to front of CRT housing
            front_offset = rot_mat @ mathutils.Vector((0.0, -crt_d / 2.0 - 0.005, 0.0))
            v.co.x += -desk_w * 0.10 + front_offset.x
            v.co.y += crt_base_y + front_offset.y
            v.co.z += crt_base_z + front_offset.z

        if self.config.screen_color == "amber":
            screen_rect = PS1TextureAtlas.get_rect("crt_screen_amber")
            screen_rgba = (0.9, 0.6, 0.1, 1.0)
        elif self.config.screen_color == "green":
            screen_rect = PS1TextureAtlas.get_rect("crt_screen_green")
            screen_rgba = (0.1, 0.85, 0.3, 1.0)
        else:
            screen_rect = PS1TextureAtlas.get_rect("crt_screen_off")
            screen_rgba = (0.05, 0.05, 0.05, 1.0)

        for f in bm.faces:
            if all(v in s_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, screen_mat, screen_rgba, col_layer)
                MeshBuilder.apply_face_uv_rect(f, uv_layer, screen_rect)

        # 4. Side magnetic tape telemetry drive / gauge
        if self.config.has_side_tape_drive:
            tape_x = desk_w * 0.25
            tape_z = shelf_z + con_h + 0.18
            MeshBuilder.add_box(
                bm,
                size=(0.20, 0.28, 0.34),
                offset=(tape_x, crt_base_y, tape_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Dual tape reel hubs
            for ry in (-0.06, 0.06):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.05,
                    depth=0.03,
                    segments=8,
                    offset=(tape_x, crt_base_y + ry, tape_z + 0.02),
                    axis='X',
                    mat_idx=metal_mat,
                    rgba=(0.85, 0.85, 0.90, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # 5. Potentiometer dials and buttons
        if self.config.has_rotary_dials:
            for dx, dcol in [(-0.06, "button_red"), (0.0, "button_yellow"), (0.06, "button_blue")]:
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.018,
                    depth=0.02,
                    segments=6,
                    offset=(desk_w * 0.18 + dx, -desk_d * 0.02, shelf_z + con_h + 0.015),
                    axis='Z',
                    mat_idx=screen_mat,
                    rgba=(0.8, 0.8, 0.8, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect(dcol)
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
