import math
import mathutils
import bmesh
import bpy

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import BunkBedConfig

class BunkBedGenerator(BaseAssetGenerator):
    """Procedural generator for double-decker stacked crew bunk beds."""

    def generate(self, config: BunkBedConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        w = config.width
        l = config.length
        h = config.height
        half_w = w * 0.5
        half_l = l * 0.5

        # Materials
        m_frame = mat_mgr.get_index("wall_support_beam")
        r_frame = mat_mgr.get_rect("metal_light_brushed")

        m_dark = mat_mgr.get_index("wall_bulkhead")
        r_dark = mat_mgr.get_rect("metal_dark_grime")

        m_mattress = mat_mgr.get_index("mat_casing")
        r_mattress = mat_mgr.get_rect("beige_plastic_worn")

        m_pillow = mat_mgr.get_index("button_gray")
        r_pillow = mat_mgr.get_rect("beige_plastic_worn")

        m_stain = mat_mgr.get_index("rust_patch")
        r_stain = mat_mgr.get_rect("rust_heavy")

        m_light = mat_mgr.get_index("fluorescent_tube_lit")
        r_light = mat_mgr.get_rect("fluorescent_lit")

        if config.blanket_color == "medical_blue":
            m_blanket = mat_mgr.get_index("chemical_barrel_blue")
            r_blanket = mat_mgr.get_rect("button_blue")
            blanket_rgba = (0.15, 0.35, 0.55, 1.0)
        elif config.blanket_color == "emergency_orange":
            m_blanket = mat_mgr.get_index("hazard_yellow")
            r_blanket = mat_mgr.get_rect("hazard_stripes")
            blanket_rgba = (0.85, 0.55, 0.10, 1.0)
        elif config.blanket_color == "brown_wool":
            m_blanket = mat_mgr.get_index("chair_vinyl")
            r_blanket = mat_mgr.get_rect("chair_vinyl_dark")
            blanket_rgba = (0.28, 0.22, 0.18, 1.0)
        else: # station_gray
            m_blanket = mat_mgr.get_index("locker_gray")
            r_blanket = mat_mgr.get_rect("metal_dark_grime")
            blanket_rgba = (0.35, 0.37, 0.40, 1.0)

        # -------------------------------------------------------------
        # 1. STRUCTURAL POSTS & FRAMEWORK
        # -------------------------------------------------------------
        post_thick = 0.05 if config.frame_style == "tubular_metal" else 0.075

        # 4 Corner Upright Posts
        for px in [-half_w + post_thick * 0.5, half_w - post_thick * 0.5]:
            for py in [-half_l + post_thick * 0.5, half_l - post_thick * 0.5]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((post_thick, post_thick, h)),
                    offset=mathutils.Vector((px, py, h * 0.5)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer,
                    rgba=(0.35, 0.38, 0.40, 1.0)
                )

        # Top Cross Ties
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, post_thick, post_thick)),
            offset=mathutils.Vector((0.0, half_l - post_thick * 0.5, h - post_thick * 0.5)),
            mat_idx=m_frame,
            uv_layer=uv_layer,
            uv_rect=r_frame,
            color_layer=color_layer
        )
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, post_thick, post_thick)),
            offset=mathutils.Vector((0.0, -half_l + post_thick * 0.5, h - post_thick * 0.5)),
            mat_idx=m_frame,
            uv_layer=uv_layer,
            uv_rect=r_frame,
            color_layer=color_layer
        )

        # Capsule / Bulkhead Enclosure Panels
        if config.frame_style in ["capsule_stacked", "reinforced_bulkhead"]:
            # Back Wall (+X or +Y depending on orientation, let's enclose +X side and headboard +Y)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, 0.04, h)),
                offset=mathutils.Vector((0.0, half_l, h * 0.5)),
                mat_idx=m_dark,
                uv_layer=uv_layer,
                uv_rect=r_dark,
                color_layer=color_layer,
                rgba=(0.24, 0.26, 0.28, 1.0)
            )
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, 0.04, h * 0.70)),
                offset=mathutils.Vector((0.0, -half_l, h * 0.35)),
                mat_idx=m_dark,
                uv_layer=uv_layer,
                uv_rect=r_dark,
                color_layer=color_layer,
                rgba=(0.24, 0.26, 0.28, 1.0)
            )

        # -------------------------------------------------------------
        # 2. BUNK PLATFORMS & MATTRESSES
        # -------------------------------------------------------------
        lower_z = 0.36
        upper_z = h * 0.62
        bunk_platform_thick = 0.05
        mattress_thick = 0.14

        def build_bunk_layer(base_z: float, state: str):
            # Platform base pan
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w - 0.02, l - 0.02, bunk_platform_thick)),
                offset=mathutils.Vector((0.0, 0.0, base_z + bunk_platform_thick * 0.5)),
                mat_idx=m_dark,
                uv_layer=uv_layer,
                uv_rect=r_dark,
                color_layer=color_layer
            )
            # Longitudinal side rail
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.04, l, 0.08)),
                offset=mathutils.Vector((-half_w + 0.02, 0.0, base_z + 0.04)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.04, l, 0.08)),
                offset=mathutils.Vector((half_w - 0.02, 0.0, base_z + 0.04)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )

            # Mattress
            m_top = base_z + bunk_platform_thick + mattress_thick
            if state != "empty_storage":
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((w * 0.90, l * 0.94, mattress_thick)),
                    offset=mathutils.Vector((0.0, 0.0, base_z + bunk_platform_thick + mattress_thick * 0.5)),
                    mat_idx=m_mattress,
                    uv_layer=uv_layer,
                    uv_rect=r_mattress,
                    color_layer=color_layer,
                    rgba=(0.58, 0.56, 0.50, 1.0)
                )

                # Bedding / Blanket
                if state == "made":
                    b_len = l * 0.70
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((w * 0.92, b_len, 0.025)),
                        offset=mathutils.Vector((0.0, -half_l + b_len * 0.5 + 0.03, m_top + 0.012)),
                        mat_idx=m_blanket,
                        uv_layer=uv_layer,
                        uv_rect=r_blanket,
                        color_layer=color_layer,
                        rgba=blanket_rgba
                    )
                elif state == "disheveled":
                    b_len = l * 0.45
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((w * 0.80, b_len, 0.05)),
                        offset=mathutils.Vector((-0.05, -0.10, m_top + 0.025)),
                        mat_idx=m_blanket,
                        uv_layer=uv_layer,
                        uv_rect=r_blanket,
                        color_layer=color_layer,
                        rgba=blanket_rgba
                    )
                elif state == "bare_foam_stained":
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((w * 0.42, 0.55, 0.005)),
                        offset=mathutils.Vector((0.04, 0.05, m_top + 0.003)),
                        mat_idx=m_stain,
                        uv_layer=uv_layer,
                        uv_rect=r_stain,
                        color_layer=color_layer,
                        rgba=(0.42, 0.14, 0.10, 1.0)
                    )

                # Pillow
                p_len = 0.35
                p_w = w * 0.70
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((p_w, p_len, 0.08)),
                    offset=mathutils.Vector((0.0, half_l - p_len * 0.5 - 0.06, m_top + 0.04)),
                    mat_idx=m_pillow,
                    uv_layer=uv_layer,
                    uv_rect=r_pillow,
                    color_layer=color_layer,
                    rgba=(0.78, 0.78, 0.75, 1.0)
                )
            else: # empty_storage cargo straps
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((w * 0.88, l * 0.88, 0.01)),
                    offset=mathutils.Vector((0.0, 0.0, base_z + bunk_platform_thick + 0.005)),
                    mat_idx=m_dark,
                    uv_layer=uv_layer,
                    uv_rect=r_dark,
                    color_layer=color_layer
                )

        # Build lower bunk
        build_bunk_layer(lower_z, config.lower_bunk_state)
        # Build upper bunk
        build_bunk_layer(upper_z, config.upper_bunk_state)

        # Upper Guardrail
        if config.upper_guardrail:
            rail_h = 0.25
            rail_l = l * 0.65
            rail_z = upper_z + bunk_platform_thick + mattress_thick + rail_h * 0.5
            # Front guardrail
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.025, rail_l, 0.025)),
                offset=mathutils.Vector((-half_w + 0.02, -half_l + rail_l * 0.5 + 0.05, rail_z + rail_h * 0.5)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            # Uprights
            for uy in [-half_l + 0.06, -half_l + rail_l * 0.5, -half_l + rail_l]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.025, 0.025, rail_h)),
                    offset=mathutils.Vector((-half_w + 0.02, uy, rail_z)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )

        # -------------------------------------------------------------
        # 3. ACCESS LADDER
        # -------------------------------------------------------------
        ladder_w = 0.35
        ladder_side_thick = 0.035
        # Determine ladder X and Y coordinates
        if config.ladder_position == "front_left":
            lad_x = -half_w - 0.02
            lad_y = -half_l + ladder_w * 0.5 + 0.08
            lad_is_side = False
        elif config.ladder_position == "side_head":
            lad_x = 0.0
            lad_y = -half_l - 0.02
            lad_is_side = True
        else: # front_right
            lad_x = -half_w - 0.02
            lad_y = half_l - ladder_w * 0.5 - 0.08
            lad_is_side = False

        ladder_h = upper_z + 0.35
        if not lad_is_side:
            # Ladder on front face (-X)
            # 2 Uprights
            for ly in [lad_y - ladder_w * 0.5, lad_y + ladder_w * 0.5]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((ladder_side_thick, ladder_side_thick, ladder_h)),
                    offset=mathutils.Vector((lad_x, ly, ladder_h * 0.5)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )
            # 5 Rungs
            rung_count = 5
            for r_idx in range(rung_count):
                rz = 0.25 + (r_idx * (ladder_h - 0.30) / (rung_count - 1))
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.025, ladder_w, 0.025)),
                    offset=mathutils.Vector((lad_x, lad_y, rz)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )
        else:
            # Ladder on end footboard (-Y)
            for lx in [-ladder_w * 0.5, ladder_w * 0.5]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((ladder_side_thick, ladder_side_thick, ladder_h)),
                    offset=mathutils.Vector((lx, lad_y, ladder_h * 0.5)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )
            rung_count = 5
            for r_idx in range(rung_count):
                rz = 0.25 + (r_idx * (ladder_h - 0.30) / (rung_count - 1))
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((ladder_w, 0.025, 0.025)),
                    offset=mathutils.Vector((0.0, lad_y, rz)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )

        # -------------------------------------------------------------
        # 4. STORAGE DRAWERS & READING LIGHTS
        # -------------------------------------------------------------
        if config.has_storage_lockers:
            drw_w = w * 0.85
            drw_l = l * 0.42
            drw_h = lower_z - 0.04
            for dy in [-l * 0.22, l * 0.22]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((drw_w, drw_l, drw_h)),
                    offset=mathutils.Vector((0.0, dy, drw_h * 0.5 + 0.02)),
                    mat_idx=m_dark,
                    uv_layer=uv_layer,
                    uv_rect=r_dark,
                    color_layer=color_layer,
                    rgba=(0.28, 0.30, 0.32, 1.0)
                )
                # Pull handle
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.02, 0.18, 0.04)),
                    offset=mathutils.Vector((-drw_w * 0.5 - 0.01, dy, drw_h * 0.60)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )

        # Reading Lights
        if config.has_reading_lights:
            for l_z in [lower_z + 0.65, upper_z + 0.60]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.06, 0.08, 0.08)),
                    offset=mathutils.Vector((0.0, half_l - 0.04, l_z)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.04, 0.02, 0.04)),
                    offset=mathutils.Vector((0.0, half_l - 0.08, l_z)),
                    mat_idx=m_light,
                    uv_layer=uv_layer,
                    uv_rect=r_light,
                    color_layer=color_layer,
                    rgba=(0.95, 0.95, 0.90, 1.0)
                )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: BunkBedConfig) -> ValidationReport:
        return super().validate(obj, config)
