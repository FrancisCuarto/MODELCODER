import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import NeuralInterfaceChairConfig

class NeuralInterfaceChairGenerator(BaseAssetGenerator[NeuralInterfaceChairConfig]):
    """
    Procedural generator for Neural Interface Chair:
    Ergonomic technical procedure chair with hydraulic base, overhead sensor arch,
    electrode headrest, and wrist restraint cuffs.
    """

    def generate(self, config: NeuralInterfaceChairConfig = None) -> bpy.types.Object:
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

        seat_h = self.config.seat_height
        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        vinyl_mat = m_idx.get("casing", 0)
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        vinyl_rgba = (0.16, 0.18, 0.22, 1.0)
        casing_rgba = self.material_manager.get_rgba("casing")

        # 1. Base pedestal and floor flange
        MeshBuilder.add_box(
            bm,
            size=(0.65, 0.75, 0.05),
            offset=(0.0, 0.0, 0.025),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Hydraulic vertical cylinder
        MeshBuilder.add_cylinder(
            bm,
            radius=0.10,
            depth=seat_h - 0.05,
            segments=8,
            offset=(0.0, 0.0, (seat_h - 0.05) / 2.0 + 0.05),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Seat frame carriage
        seat_w = 0.55
        seat_d = 0.52
        seat_t = 0.10
        MeshBuilder.add_box(
            bm,
            size=(seat_w, seat_d, 0.04),
            offset=(0.0, 0.0, seat_h),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Seat cushion
        MeshBuilder.add_box(
            bm,
            size=(seat_w * 0.92, seat_d * 0.92, seat_t),
            offset=(0.0, 0.02, seat_h + seat_t / 2.0 + 0.02),
            mat_idx=vinyl_mat,
            rgba=vinyl_rgba,
            uv_rect=PS1TextureAtlas.get_rect("chair_vinyl_dark")
        )

        # 2. Backrest (tilted backwards)
        angle_rad = math.radians(self.config.backrest_angle)
        back_w = 0.50
        back_h = 0.68
        back_t = 0.08

        # Pivot point at rear of seat
        pivot_y = -seat_d / 2.0 + 0.02
        pivot_z = seat_h + 0.06
        rot_mat = mathutils.Euler((angle_rad, 0.0, 0.0), 'XYZ').to_matrix()

        back_geom = bmesh.ops.create_cube(bm, size=1.0)
        b_verts = [v for v in back_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in b_verts:
            v.co.x *= back_w
            v.co.y *= back_t
            v.co.z *= back_h
            # Translate local center relative to bottom hinge
            v.co.z += back_h / 2.0
            # Rotate
            v.co = rot_mat @ v.co
            # Translate to pivot
            v.co.y += pivot_y
            v.co.z += pivot_z

        for f in bm.faces:
            if all(v in b_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, vinyl_mat, vinyl_rgba, col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("chair_vinyl_dark"))

        # Padded headrest
        head_w = 0.26
        head_h = 0.22
        head_t = 0.09
        head_geom = bmesh.ops.create_cube(bm, size=1.0)
        h_verts = [v for v in head_geom["verts"] if isinstance(v, bmesh.types.BMVert)]
        for v in h_verts:
            v.co.x *= head_w
            v.co.y *= head_t
            v.co.z *= head_h
            v.co.z += back_h + head_h / 2.0 + 0.02
            v.co = rot_mat @ v.co
            v.co.y += pivot_y
            v.co.z += pivot_z

        for f in bm.faces:
            if all(v in h_verts for v in f.verts):
                MeshBuilder.apply_face_attributes(f, metal_mat, (0.2, 0.22, 0.26, 1.0), col_layer)
                MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("rubber_black"))

        # Headrest electrode contact nodes
        for sx in (-1, 1):
            e_node = bmesh.ops.create_cube(bm, size=1.0)
            e_verts = [v for v in e_node["verts"] if isinstance(v, bmesh.types.BMVert)]
            for v in e_verts:
                v.co.x *= 0.04
                v.co.y *= 0.04
                v.co.z *= 0.04
                v.co.x += sx * (head_w / 2.0 + 0.02)
                v.co.y += 0.02
                v.co.z += back_h + head_h / 2.0 + 0.02
                v.co = rot_mat @ v.co
                v.co.y += pivot_y
                v.co.z += pivot_z
            for f in bm.faces:
                if all(v in e_verts for v in f.verts):
                    MeshBuilder.apply_face_attributes(f, brass_mat, (0.85, 0.7, 0.2, 1.0), col_layer)
                    MeshBuilder.apply_box_face_uv(f, uv_layer, PS1TextureAtlas.get_rect("cartridge_amber"))

        # 3. Overhead cognitive sensor arch
        if self.config.has_sensor_arch:
            arch_top_z = pivot_z + (rot_mat @ mathutils.Vector((0.0, 0.0, back_h + head_h + 0.18))).z
            arch_top_y = pivot_y + (rot_mat @ mathutils.Vector((0.0, 0.0, back_h + head_h + 0.18))).y
            
            # Curved crown above head
            MeshBuilder.add_box(
                bm,
                size=(0.42, 0.12, 0.05),
                offset=(0.0, arch_top_y + 0.05, arch_top_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Electrode sensors hanging down
            for ex in (-0.14, 0.0, 0.14):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.025,
                    depth=0.06,
                    segments=6,
                    offset=(ex, arch_top_y + 0.05, arch_top_z - 0.04),
                    axis='Z',
                    mat_idx=brass_mat,
                    rgba=(0.8, 0.7, 0.2, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                )

        # 4. Armrests with restraint cuffs
        arm_h = seat_h + seat_t + 0.12
        for sx in (-1, 1):
            arm_x = sx * (seat_w / 2.0 + 0.04)
            # Support strut
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=0.18,
                segments=6,
                offset=(arm_x, 0.0, seat_h + 0.08),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Armrest pad
            MeshBuilder.add_box(
                bm,
                size=(0.09, 0.38, 0.04),
                offset=(arm_x, 0.05, arm_h),
                mat_idx=vinyl_mat,
                rgba=vinyl_rgba,
                uv_rect=PS1TextureAtlas.get_rect("chair_vinyl_dark")
            )
            if self.config.has_restraint_straps:
                # Restraint cuff clamp
                MeshBuilder.add_box(
                    bm,
                    size=(0.10, 0.07, 0.06),
                    offset=(arm_x, 0.12, arm_h + 0.03),
                    mat_idx=metal_mat,
                    rgba=(0.1, 0.1, 0.1, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

        # 5. Side operator keypad panel
        if self.config.has_side_operator_panel:
            MeshBuilder.add_box(
                bm,
                size=(0.06, 0.14, 0.12),
                offset=(seat_w / 2.0 + 0.10, 0.18, arm_h + 0.02),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Buttons
            MeshBuilder.add_box(
                bm,
                size=(0.01, 0.04, 0.04),
                offset=(seat_w / 2.0 + 0.135, 0.18, arm_h + 0.03),
                mat_idx=screen_mat,
                rgba=(0.9, 0.2, 0.2, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        # 6. Umbilical cables running to floor
        if self.config.has_umbilical_cables:
            cable_top = pivot_z + (rot_mat @ mathutils.Vector((0.0, 0.0, back_h * 0.8))).z
            cable_y = pivot_y + (rot_mat @ mathutils.Vector((0.0, 0.0, back_h * 0.8))).y
            MeshBuilder.add_cylinder(
                bm,
                radius=0.02,
                depth=cable_top - 0.05,
                segments=6,
                offset=(0.0, cable_y - 0.08, (cable_top - 0.05) / 2.0 + 0.05),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.08, 0.08, 0.08, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
