import math
import mathutils
import bmesh
import bpy

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import CrewBedConfig

class CrewBedGenerator(BaseAssetGenerator):
    """Procedural generator for PSX-style station beds, cots, and infirmary gurneys."""

    def generate(self, config: CrewBedConfig) -> bpy.types.Object:
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

        # Blanket color
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

        m_pillow = mat_mgr.get_index("button_gray")
        r_pillow = mat_mgr.get_rect("beige_plastic_worn")

        m_stain = mat_mgr.get_index("rust_patch")
        r_stain = mat_mgr.get_rect("rust_heavy")

        m_rubber = mat_mgr.get_index("rubber_tire")
        r_rubber = mat_mgr.get_rect("rubber_black")

        frame_h = h * 0.55
        mattress_thick = 0.16

        # -------------------------------------------------------------
        # 1. BED FRAME & LEGS
        # -------------------------------------------------------------
        if config.bed_type == "enclosed_pod":
            # Solid boxy bulkhead pod frame with headboard and footboard
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + 0.08, l + 0.12, frame_h)),
                offset=mathutils.Vector((0.0, 0.0, frame_h * 0.5)),
                mat_idx=m_dark,
                uv_layer=uv_layer,
                uv_rect=r_dark,
                color_layer=color_layer,
                rgba=(0.22, 0.24, 0.26, 1.0)
            )
            # Tall Headboard
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + 0.08, 0.12, h + 0.35)),
                offset=mathutils.Vector((0.0, half_l + 0.06, (h + 0.35) * 0.5)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer,
                rgba=(0.32, 0.35, 0.38, 1.0)
            )
            # Footboard
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + 0.08, 0.08, h + 0.10)),
                offset=mathutils.Vector((0.0, -half_l - 0.04, (h + 0.10) * 0.5)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )

        elif config.bed_type == "medical_gurney":
            # Central pedestal with wheels and scissor struts
            pedestal_w = w * 0.55
            pedestal_l = l * 0.70
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((pedestal_w, pedestal_l, 0.08)),
                offset=mathutils.Vector((0.0, 0.0, 0.14)),
                mat_idx=m_dark,
                uv_layer=uv_layer,
                uv_rect=r_dark,
                color_layer=color_layer
            )
            # Hydraulic central column
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.25, 0.40, frame_h - 0.14)),
                offset=mathutils.Vector((0.0, 0.0, 0.14 + (frame_h - 0.14) * 0.5)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            # 4 Caster Wheels
            wheel_rad = 0.06
            for cx in [-pedestal_w * 0.42, pedestal_w * 0.42]:
                for cy in [-pedestal_l * 0.42, pedestal_l * 0.42]:
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=wheel_rad,
                        depth=0.04,
                        segments=6,
                        offset=mathutils.Vector((cx, cy, wheel_rad)),
                        axis='X',
                        mat_idx=m_rubber,
                        uv_layer=uv_layer,
                        uv_rect=r_rubber,
                        color_layer=color_layer
                    )
            # Mattress pan
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + 0.04, l + 0.04, 0.06)),
                offset=mathutils.Vector((0.0, 0.0, frame_h + 0.03)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )

        else: # crew_cot (tubular steel 4-legged cot)
            leg_thick = 0.045
            for lx in [-half_w + 0.03, half_w - 0.03]:
                for ly in [-half_l + 0.03, half_l - 0.03]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((leg_thick, leg_thick, frame_h)),
                        offset=mathutils.Vector((lx, ly, frame_h * 0.5)),
                        mat_idx=m_frame,
                        uv_layer=uv_layer,
                        uv_rect=r_frame,
                        color_layer=color_layer
                    )
            # Longitudinal side rails
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((leg_thick, l, 0.06)),
                offset=mathutils.Vector((-half_w + 0.03, 0.0, frame_h - 0.03)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((leg_thick, l, 0.06)),
                offset=mathutils.Vector((half_w - 0.03, 0.0, frame_h - 0.03)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            # Headboard & Footboard arches
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, leg_thick, 0.35)),
                offset=mathutils.Vector((0.0, half_l - 0.03, frame_h + 0.14)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, leg_thick, 0.20)),
                offset=mathutils.Vector((0.0, -half_l + 0.03, frame_h + 0.08)),
                mat_idx=m_frame,
                uv_layer=uv_layer,
                uv_rect=r_frame,
                color_layer=color_layer
            )

        # Under-bed drawers
        if config.has_under_drawers and config.bed_type != "medical_gurney":
            drw_w = w * 0.82
            drw_l = l * 0.38
            drw_h = frame_h * 0.70
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
                # Recessed handle lip
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.02, 0.20, 0.04)),
                    offset=mathutils.Vector((-drw_w * 0.5 - 0.01, dy, drw_h * 0.65)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )

        # -------------------------------------------------------------
        # 2. MATTRESS
        # -------------------------------------------------------------
        mat_z = frame_h + mattress_thick * 0.5
        if config.headrest_incline > 1.0:
            # Split mattress: lower 2/3 flat, upper 1/3 inclined
            flat_l = l * 0.65
            head_l = l * 0.35
            # Flat part
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.94, flat_l, mattress_thick)),
                offset=mathutils.Vector((0.0, -half_l + flat_l * 0.5, mat_z)),
                mat_idx=m_mattress,
                uv_layer=uv_layer,
                uv_rect=r_mattress,
                color_layer=color_layer,
                rgba=(0.60, 0.58, 0.52, 1.0)
            )
            # Inclined head part
            inc_rad = math.radians(min(45.0, config.headrest_incline))
            head_z_lift = math.sin(inc_rad) * (head_l * 0.5)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.94, head_l, mattress_thick)),
                offset=mathutils.Vector((0.0, half_l - head_l * 0.5, mat_z + head_z_lift)),
                mat_idx=m_mattress,
                uv_layer=uv_layer,
                uv_rect=r_mattress,
                color_layer=color_layer,
                rgba=(0.60, 0.58, 0.52, 1.0)
            )
        else:
            # Full flat mattress
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.94, l * 0.96, mattress_thick)),
                offset=mathutils.Vector((0.0, 0.0, mat_z)),
                mat_idx=m_mattress,
                uv_layer=uv_layer,
                uv_rect=r_mattress,
                color_layer=color_layer,
                rgba=(0.60, 0.58, 0.52, 1.0)
            )

        # -------------------------------------------------------------
        # 3. BEDDING, BLANKET & PILLOW
        # -------------------------------------------------------------
        top_z = frame_h + mattress_thick

        if config.mattress_state == "made_clean":
            # Neatly tucked blanket covering lower 70% of bed
            b_len = l * 0.72
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.96, b_len, 0.03)),
                offset=mathutils.Vector((0.0, -half_l + b_len * 0.5, top_z + 0.015)),
                mat_idx=m_blanket,
                uv_layer=uv_layer,
                uv_rect=r_blanket,
                color_layer=color_layer,
                rgba=blanket_rgba
            )
            # Folded sheet cuff
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.96, 0.12, 0.035)),
                offset=mathutils.Vector((0.0, -half_l + b_len, top_z + 0.017)),
                mat_idx=m_pillow,
                uv_layer=uv_layer,
                uv_rect=r_pillow,
                color_layer=color_layer,
                rgba=(0.75, 0.75, 0.72, 1.0)
            )

        elif config.mattress_state == "rumpled_disheveled":
            # Disordered bunched blanket thrown across the middle
            b_len = l * 0.50
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.85, b_len, 0.06)),
                offset=mathutils.Vector((0.05, -0.15, top_z + 0.03)),
                mat_idx=m_blanket,
                uv_layer=uv_layer,
                uv_rect=r_blanket,
                color_layer=color_layer,
                rgba=blanket_rgba
            )
            # Second bunched fold
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.55, 0.35, 0.08)),
                offset=mathutils.Vector((-0.10, -0.35, top_z + 0.05)),
                mat_idx=m_blanket,
                uv_layer=uv_layer,
                uv_rect=r_blanket,
                color_layer=color_layer,
                rgba=blanket_rgba
            )

        elif config.mattress_state == "bare_foam_stained":
            # Dark grim/blood stain on bare foam
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.45, 0.65, 0.005)),
                offset=mathutils.Vector((0.05, 0.10, top_z + 0.002)),
                mat_idx=m_stain,
                uv_layer=uv_layer,
                uv_rect=r_stain,
                color_layer=color_layer,
                rgba=(0.45, 0.15, 0.10, 1.0)
            )

        # Pillow
        if config.has_pillow:
            p_len = 0.38
            p_width = w * 0.75
            p_thick = 0.09
            p_y = half_l - p_len * 0.5 - 0.06
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((p_width, p_len, p_thick)),
                offset=mathutils.Vector((0.0, p_y, top_z + p_thick * 0.5)),
                mat_idx=m_pillow,
                uv_layer=uv_layer,
                uv_rect=r_pillow,
                color_layer=color_layer,
                rgba=(0.78, 0.78, 0.75, 1.0)
            )

        # Side Guardrails
        if config.has_guardrails or config.bed_type == "medical_gurney":
            rail_l = l * 0.65
            rail_h = 0.22
            rail_thick = 0.025
            for rx in [-half_w - 0.015, half_w + 0.015]:
                # Top rail
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((rail_thick, rail_l, rail_thick)),
                    offset=mathutils.Vector((rx, 0.0, top_z + rail_h)),
                    mat_idx=m_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_frame,
                    color_layer=color_layer
                )
                # Vertical uprights
                for ry in [-rail_l * 0.42, 0.0, rail_l * 0.42]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((rail_thick, rail_thick, rail_h)),
                        offset=mathutils.Vector((rx, ry, top_z + rail_h * 0.5)),
                        mat_idx=m_frame,
                        uv_layer=uv_layer,
                        uv_rect=r_frame,
                        color_layer=color_layer
                    )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: CrewBedConfig) -> ValidationReport:
        return super().validate(obj, config)
