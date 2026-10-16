import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import DeconChamberConfig

class DeconChamberGenerator(BaseAssetGenerator[DeconChamberConfig]):
    """
    Procedural generator for Decon Chamber:
    Chemical decontamination shower booth with multiple spray nozzle tiers,
    deluge ceiling head, floor sump grate, and external cycle status console.
    """

    def generate(self, config: DeconChamberConfig = None) -> bpy.types.Object:
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

        w = self.config.chamber_width
        d = self.config.chamber_depth
        h = self.config.chamber_height

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        pipe_mat = m_idx.get("pipe", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        glass_rgba = (0.35, 0.65, 0.75, 0.75)

        wall_t = 0.08
        base_h = 0.14

        # 1. Base drainage sump & walking grating
        MeshBuilder.add_box(
            bm,
            size=(w, d, base_h),
            offset=(0.0, 0.0, base_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        MeshBuilder.add_box(
            bm,
            size=(w * 0.75, d * 0.75, 0.02),
            offset=(0.0, 0.0, base_h + 0.01),
            mat_idx=metal_mat,
            rgba=(0.25, 0.25, 0.28, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("vent_grill")
        )

        cabin_h = h - base_h - 0.16
        cabin_z = base_h + cabin_h / 2.0

        # 2. Back and side walls
        # Back wall
        MeshBuilder.add_box(
            bm,
            size=(w, wall_t, cabin_h),
            offset=(0.0, -d / 2.0 + wall_t / 2.0, cabin_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
        )

        # Left and Right walls
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(wall_t, d - wall_t, cabin_h),
                offset=(sx * (w / 2.0 - wall_t / 2.0), wall_t / 2.0, cabin_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("ceramic_tile_white")
            )

        # 3. Top roof ceiling slab & deluge shower head
        roof_h = 0.16
        roof_z = base_h + cabin_h + roof_h / 2.0
        MeshBuilder.add_box(
            bm,
            size=(w * 1.04, d * 1.04, roof_h),
            offset=(0.0, 0.0, roof_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        if self.config.has_ceiling_shower_head:
            # Ceiling shower rose head
            MeshBuilder.add_cylinder(
                bm,
                radius=0.14,
                depth=0.06,
                segments=8,
                offset=(0.0, 0.0, base_h + cabin_h - 0.03),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.8, 0.82, 0.85, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # 4. Vertical corner chemical pipes & spray nozzles
        tiers = max(2, min(4, int(self.config.nozzle_tiers)))
        for sx in (-1, 1):
            pipe_x = sx * (w / 2.0 - wall_t - 0.06)
            pipe_y = -d / 2.0 + wall_t + 0.06
            # Vertical manifold pipe
            MeshBuilder.add_cylinder(
                bm,
                radius=0.02,
                depth=cabin_h * 0.9,
                segments=6,
                offset=(pipe_x, pipe_y, cabin_z),
                axis='Z',
                mat_idx=pipe_mat,
                rgba=(0.4, 0.45, 0.5, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Spray nozzles at each height tier
            for t in range(tiers):
                nz_z = base_h + 0.35 + t * (cabin_h * 0.75 / float(tiers))
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.015,
                    depth=0.06,
                    segments=4,
                    offset=(pipe_x - sx * 0.03, pipe_y + 0.03, nz_z),
                    axis='X',
                    mat_idx=brass_mat,
                    rgba=(0.85, 0.68, 0.22, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                )

        # 5. Front door hatch with hinge rotation
        angle_rad = math.radians(self.config.door_open_angle)
        door_w = w * 0.88
        door_h = cabin_h * 0.96
        door_t = 0.06
        hinge_x = -w / 2.0 + wall_t
        hinge_y = d / 2.0 - door_t / 2.0

        door_rot = mathutils.Euler((0.0, 0.0, -angle_rad), 'XYZ')
        local_door_offset = mathutils.Vector((door_w / 2.0, 0.0, 0.0))
        rotated_door_offset = door_rot.to_matrix() @ local_door_offset
        door_center = mathutils.Vector((hinge_x, hinge_y, cabin_z)) + rotated_door_offset

        # Door frame
        door_geom = bmesh.ops.create_cube(bm, size=1.0)
        d_verts = [v for v in door_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in d_verts:
            v.co.x *= door_w
            v.co.y *= door_t
            v.co.z *= door_h
            v.co = door_rot.to_matrix() @ v.co
            v.co += door_center

        for f in bm.faces:
            if all(v in d_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, casing_mat, casing_rgba, col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("painted_metal_white"))

        # Door observation window
        win_w = door_w * 0.45
        win_h = door_h * 0.50
        win_geom = bmesh.ops.create_cube(bm, size=1.0)
        w_verts = [v for v in win_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in w_verts:
            v.co.x *= win_w
            v.co.y *= door_t * 1.2
            v.co.z *= win_h
            v.co = door_rot.to_matrix() @ v.co
            v.co += door_center + door_rot.to_matrix() @ mathutils.Vector((0.0, 0.0, cabin_h * 0.08))

        for f in bm.faces:
            if all(v in w_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, glass_mat, glass_rgba, col_layer)
                MeshBuilder.apply_face_uv_rect(f, uv_layer, PS1TextureAtlas.get_rect("glass_reinforced"))

        # 6. External cycle control panel on side wall
        if self.config.has_external_cycle_panel:
            panel_x = w / 2.0 + 0.03
            panel_z = cabin_z + 0.10
            MeshBuilder.add_box(
                bm,
                size=(0.06, 0.22, 0.32),
                offset=(panel_x, 0.15, panel_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Cycle status screen
            if self.config.cycle_state == "active":
                scr_rect = PS1TextureAtlas.get_rect("oxygen_cyan_glow")
                scr_rgba = (0.2, 0.8, 0.9, 1.0)
            elif self.config.cycle_state == "alarm":
                scr_rect = PS1TextureAtlas.get_rect("led_red")
                scr_rgba = (0.9, 0.15, 0.15, 1.0)
            else:
                scr_rect = PS1TextureAtlas.get_rect("crt_screen_green")
                scr_rgba = (0.1, 0.85, 0.25, 1.0)

            MeshBuilder.add_box(
                bm,
                size=(0.01, 0.16, 0.12),
                offset=(panel_x + 0.031, 0.15, panel_z + 0.06),
                mat_idx=screen_mat,
                rgba=scr_rgba,
                uv_rect=scr_rect
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
