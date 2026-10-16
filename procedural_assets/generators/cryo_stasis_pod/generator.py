import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CryoStasisPodConfig

class CryoStasisPodGenerator(BaseAssetGenerator[CryoStasisPodConfig]):
    """
    Procedural generator for Cryo Stasis Pod:
    Industrial retrofuturistic cryo-preservation chamber with heavy steel hatch,
    inspection window, cooling conduits, and life support readouts.
    """

    def generate(self, config: CryoStasisPodConfig = None) -> bpy.types.Object:
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

        h = self.config.height
        w = self.config.width
        d = self.config.depth

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        pipe_mat = m_idx.get("pipe", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        glass_rgba = (0.35, 0.65, 0.75, 0.85) if self.config.pod_state != "offline" else (0.2, 0.25, 0.25, 0.9)
        screen_rgba = (0.1, 0.8, 0.3, 1.0) if self.config.pod_state != "offline" else (0.05, 0.05, 0.05, 1.0)

        # 1. Base pedestal (heavy octagonal foundation plate)
        base_h = 0.15
        MeshBuilder.add_box(
            bm,
            size=(w * 1.1, d * 1.1, base_h),
            offset=(0.0, 0.0, base_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 2. Main vertical chamber shell (rear and side enclosure)
        chamber_h = h - base_h - 0.2
        chamber_z = base_h + chamber_h / 2.0
        wall_t = 0.1

        # Rear back wall
        MeshBuilder.add_box(
            bm,
            size=(w, wall_t, chamber_h),
            offset=(0.0, -d / 2.0 + wall_t / 2.0, chamber_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Left and Right walls
        side_d = d - wall_t
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(wall_t, side_d, chamber_h),
                offset=(sx * (w / 2.0 - wall_t / 2.0), -wall_t / 2.0, chamber_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # Interior rear padding / stasis cradle
        MeshBuilder.add_box(
            bm,
            size=(w * 0.7, 0.06, chamber_h * 0.88),
            offset=(0.0, -d / 2.0 + wall_t + 0.03, chamber_z),
            mat_idx=metal_mat,
            rgba=(0.18, 0.20, 0.22, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("chair_vinyl_dark")
        )

        # Occupant cocoon silhouette (if occupied)
        if self.config.pod_state == "occupied":
            MeshBuilder.add_box(
                bm,
                size=(w * 0.45, d * 0.35, chamber_h * 0.72),
                offset=(0.0, -0.05, chamber_z - 0.05),
                mat_idx=metal_mat,
                rgba=(0.12, 0.15, 0.18, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        # Top cap manifold
        cap_h = 0.2
        cap_z = base_h + chamber_h + cap_h / 2.0
        MeshBuilder.add_box(
            bm,
            size=(w * 1.08, d * 1.08, cap_h),
            offset=(0.0, 0.0, cap_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Top warning beacon / stasis status ring
        beacon_rect = PS1TextureAtlas.get_rect("oxygen_cyan_glow") if self.config.pod_state != "offline" else PS1TextureAtlas.get_rect("crt_screen_off")
        MeshBuilder.add_cylinder(
            bm,
            radius=w * 0.22,
            depth=0.08,
            segments=8,
            offset=(0.0, 0.0, h + 0.04),
            axis='Z',
            mat_idx=screen_mat,
            rgba=screen_rgba,
            uv_rect=beacon_rect
        )

        # 3. Front door hatch with hinge rotation
        angle_rad = math.radians(self.config.door_open_angle)
        door_w = w * 0.96
        door_h = chamber_h * 0.98
        door_t = 0.09
        hinge_x = -w / 2.0 + wall_t / 2.0
        hinge_y = d / 2.0 - door_t / 2.0

        # Construct door frame relative to hinge
        # When angle == 0, door center is at (0, hinge_y, chamber_z)
        door_rot = mathutils.Euler((0.0, 0.0, -angle_rad), 'XYZ')
        
        # Local vector from hinge to door center
        local_door_offset = mathutils.Vector((w / 2.0 - wall_t / 2.0, 0.0, 0.0))
        rotated_door_offset = door_rot.to_matrix() @ local_door_offset
        door_center = mathutils.Vector((hinge_x, hinge_y, chamber_z)) + rotated_door_offset

        # Door outer body
        door_geom = bmesh.ops.create_cube(bm, size=1.0)
        d_verts = [v for v in door_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in d_verts:
            # Scale locally
            v.co.x *= door_w
            v.co.y *= door_t
            v.co.z *= door_h
            # Rotate around Z by -angle_rad
            v.co = door_rot.to_matrix() @ v.co
            # Translate to door center
            v.co += door_center

        for f in bm.faces:
            if all(v in d_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, casing_mat, casing_rgba, col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("painted_metal_white"))

        # Inspection window on door
        win_w = door_w * 0.4
        win_h = door_h * 0.55
        win_geom = bmesh.ops.create_cube(bm, size=1.0)
        w_verts = [v for v in win_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in w_verts:
            v.co.x *= win_w
            v.co.y *= door_t * 1.15
            v.co.z *= win_h
            v.co = door_rot.to_matrix() @ v.co
            v.co += door_center + door_rot.to_matrix() @ mathutils.Vector((0.0, 0.0, chamber_h * 0.08))

        frost_rect = PS1TextureAtlas.get_rect("glass_reinforced") if self.config.frost_level < 0.6 else PS1TextureAtlas.get_rect("oxygen_cyan_glow")
        for f in bm.faces:
            if all(v in w_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, glass_mat, glass_rgba, col_layer)
                MeshBuilder.apply_face_uv_rect(f, uv_layer, frost_rect)

        # 4. Cryo pipes on side
        if self.config.has_cryo_pipes:
            pipe_x = w / 2.0 + 0.04
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=chamber_h * 0.9,
                segments=6,
                offset=(pipe_x, -d * 0.15, chamber_z),
                axis='Z',
                mat_idx=pipe_mat,
                rgba=(0.35, 0.40, 0.45, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=chamber_h * 0.85,
                segments=6,
                offset=(pipe_x, d * 0.15, chamber_z),
                axis='Z',
                mat_idx=brass_mat,
                rgba=(0.75, 0.65, 0.25, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )

        # 5. Side status monitor
        if self.config.has_status_monitor:
            mon_x = -(w / 2.0 + 0.05)
            MeshBuilder.add_box(
                bm,
                size=(0.08, 0.25, 0.35),
                offset=(mon_x, 0.0, chamber_z + 0.2),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Screen face
            MeshBuilder.add_box(
                bm,
                size=(0.01, 0.20, 0.28),
                offset=(mon_x - 0.04, 0.0, chamber_z + 0.2),
                mat_idx=screen_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
