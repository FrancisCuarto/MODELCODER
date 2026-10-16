import math
import mathutils
import bmesh
import bpy
from typing import List, Dict, Any

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import StationCorridorConfig

class StationCorridorGenerator(BaseAssetGenerator):
    """Procedural generator for modular PSX-style space station corridor modules."""

    def generate(self, config: StationCorridorConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        rng = mathutils.noise.random_unit_vector  # Seeded via python random if needed
        import random
        prng = random.Random(config.seed)

        w = config.width
        l = config.length
        h = config.height
        half_w = w * 0.5
        half_l = l * 0.5

        # Pre-fetch material indices and UV rects
        m_floor = mat_mgr.get_index("floor_metal")
        r_floor = mat_mgr.get_rect("metal_dark_grime")

        m_hazard = mat_mgr.get_index("floor_hazard")
        r_hazard = mat_mgr.get_rect("hazard_stripes")

        m_grate = mat_mgr.get_index("floor_grate")
        r_grate = mat_mgr.get_rect("vent_grill")

        m_wall = mat_mgr.get_index("wall_bulkhead")
        r_wall = mat_mgr.get_rect("metal_dark_grime")

        m_beam = mat_mgr.get_index("wall_support_beam")
        r_beam = mat_mgr.get_rect("metal_light_brushed")

        m_girder = mat_mgr.get_index("ceiling_girder")
        r_girder = mat_mgr.get_rect("metal_light_brushed")

        m_door_frame = mat_mgr.get_index("door_emergency_red")
        r_door_frame = mat_mgr.get_rect("door_seal_red")

        m_rust = mat_mgr.get_index("rust_patch")
        r_rust = mat_mgr.get_rect("rust_heavy")

        m_light = mat_mgr.get_index("fluorescent_tube_lit")
        r_light = mat_mgr.get_rect("fluorescent_lit")
        if config.lighting_state == "emergency_red":
            m_light = mat_mgr.get_index("led_red")
            r_light = mat_mgr.get_rect("led_red")
        elif config.lighting_state == "unlit":
            m_light = mat_mgr.get_index("glass_tube")
            r_light = mat_mgr.get_rect("glass_reinforced")

        m_rubber = mat_mgr.get_index("rubber_tire")
        r_rubber = mat_mgr.get_rect("rubber_black")

        # -------------------------------------------------------------
        # 1. FLOOR GENERATION
        # -------------------------------------------------------------
        # Base floor slab
        floor_thickness = 0.08
        floor_size_x = w
        floor_size_y = l
        if config.corridor_type in ["t_junction", "cross_junction"]:
            floor_size_x = w + (w * 0.5 if config.corridor_type == "t_junction" else w)

        floor_offset_x = 0.0
        if config.corridor_type == "t_junction":
            floor_offset_x = w * 0.25

        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((floor_size_x, floor_size_y, floor_thickness)),
            offset=mathutils.Vector((floor_offset_x, 0.0, -floor_thickness * 0.5)),
            mat_idx=m_floor,
            uv_layer=uv_layer,
            uv_rect=r_floor,
            color_layer=color_layer,
            rgba=(0.25, 0.27, 0.29, 1.0)
        )

        # Floor hazard stripes along borders
        if config.has_hazard_stripes and config.corridor_type != "cross_junction":
            stripe_w = 0.22
            # Left stripe
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((stripe_w, l, 0.005)),
                offset=mathutils.Vector((-half_w + stripe_w * 0.5, 0.0, 0.002)),
                mat_idx=m_hazard,
                uv_layer=uv_layer,
                uv_rect=r_hazard,
                color_layer=color_layer,
                rgba=(0.85, 0.65, 0.10, 1.0)
            )
            # Right stripe (only if right side isn't fully open for T junction)
            if config.corridor_type != "t_junction":
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((stripe_w, l, 0.005)),
                    offset=mathutils.Vector((half_w - stripe_w * 0.5, 0.0, 0.002)),
                    mat_idx=m_hazard,
                    uv_layer=uv_layer,
                    uv_rect=r_hazard,
                    color_layer=color_layer,
                    rgba=(0.85, 0.65, 0.10, 1.0)
                )

        # Grated central drainage trench
        if config.floor_style == "grated_trench":
            trench_w = min(0.85, w * 0.35)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((trench_w, l * 0.90, 0.006)),
                offset=mathutils.Vector((0.0, 0.0, 0.003)),
                mat_idx=m_grate,
                uv_layer=uv_layer,
                uv_rect=r_grate,
                color_layer=color_layer,
                rgba=(0.20, 0.20, 0.22, 1.0)
            )

        # Damage: Blood / Oil Stain on floor
        if config.damage_state == "blood_oil_stain":
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.75, 1.10, 0.004)),
                offset=mathutils.Vector((prng.uniform(-0.3, 0.3), prng.uniform(-0.5, 0.5), 0.003)),
                mat_idx=m_rust,
                uv_layer=uv_layer,
                uv_rect=r_rust,
                color_layer=color_layer,
                rgba=(0.40, 0.12, 0.08, 1.0)
            )

        # -------------------------------------------------------------
        # 2. WALL GENERATION
        # -------------------------------------------------------------
        wall_thick = 0.16

        def build_straight_walls():
            # Left Wall (-X)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, l, h)),
                offset=mathutils.Vector((-half_w - wall_thick * 0.5, 0.0, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer,
                rgba=(0.28, 0.30, 0.32, 1.0)
            )
            # Right Wall (+X)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, l, h)),
                offset=mathutils.Vector((half_w + wall_thick * 0.5, 0.0, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer,
                rgba=(0.28, 0.30, 0.32, 1.0)
            )

            # Structural support columns / ribs
            if config.wall_style == "structural_ribs":
                rib_depth = 0.16
                rib_w = 0.25
                for y_pos in [-half_l * 0.45, half_l * 0.45]:
                    # Left Rib
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((rib_depth, rib_w, h)),
                        offset=mathutils.Vector((-half_w + rib_depth * 0.5, y_pos, h * 0.5)),
                        mat_idx=m_beam,
                        uv_layer=uv_layer,
                        uv_rect=r_beam,
                        color_layer=color_layer,
                        rgba=(0.35, 0.38, 0.40, 1.0)
                    )
                    # Right Rib
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((rib_depth, rib_w, h)),
                        offset=mathutils.Vector((half_w - rib_depth * 0.5, y_pos, h * 0.5)),
                        mat_idx=m_beam,
                        uv_layer=uv_layer,
                        uv_rect=r_beam,
                        color_layer=color_layer,
                        rgba=(0.35, 0.38, 0.40, 1.0)
                    )

            # Wall niche / equipment alcove
            if config.has_wall_alcove:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.08, 0.90, 1.20)),
                    offset=mathutils.Vector((-half_w + 0.04, 0.0, 1.20)),
                    mat_idx=m_beam,
                    uv_layer=uv_layer,
                    uv_rect=r_beam,
                    color_layer=color_layer,
                    rgba=(0.20, 0.22, 0.24, 1.0)
                )

        if config.corridor_type in ["straight", "doorway_arch"]:
            build_straight_walls()
            if config.corridor_type == "doorway_arch":
                # Heavy bulkhead frame arch dividing the corridor at y=0
                jamb_w = (w - config.doorway_width) * 0.5
                lintel_h = h - config.doorway_height
                frame_thick = 0.35
                # Left jamb
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((jamb_w, frame_thick, config.doorway_height)),
                    offset=mathutils.Vector((-half_w + jamb_w * 0.5, 0.0, config.doorway_height * 0.5)),
                    mat_idx=m_door_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_door_frame,
                    color_layer=color_layer,
                    rgba=(0.58, 0.10, 0.08, 1.0)
                )
                # Right jamb
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((jamb_w, frame_thick, config.doorway_height)),
                    offset=mathutils.Vector((half_w - jamb_w * 0.5, 0.0, config.doorway_height * 0.5)),
                    mat_idx=m_door_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_door_frame,
                    color_layer=color_layer,
                    rgba=(0.58, 0.10, 0.08, 1.0)
                )
                # Lintel header
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((w, frame_thick, lintel_h)),
                    offset=mathutils.Vector((0.0, 0.0, config.doorway_height + lintel_h * 0.5)),
                    mat_idx=m_door_frame,
                    uv_layer=uv_layer,
                    uv_rect=r_door_frame,
                    color_layer=color_layer,
                    rgba=(0.58, 0.10, 0.08, 1.0)
                )

        elif config.corridor_type == "dead_end":
            build_straight_walls()
            # North End Wall (+Y)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + wall_thick * 2.0, wall_thick, h)),
                offset=mathutils.Vector((0.0, half_l + wall_thick * 0.5, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer,
                rgba=(0.28, 0.30, 0.32, 1.0)
            )
            # Maintenance hatch on end wall
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((1.0, 0.05, 1.4)),
                offset=mathutils.Vector((0.0, half_l - 0.02, 1.1)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer,
                rgba=(0.35, 0.38, 0.40, 1.0)
            )

        elif config.corridor_type == "corner_90":
            # Turn from -Y to +X
            # Outer wall (-X)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, l + wall_thick, h)),
                offset=mathutils.Vector((-half_w - wall_thick * 0.5, wall_thick * 0.5, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer
            )
            # Outer wall (+Y)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w + wall_thick, wall_thick, h)),
                offset=mathutils.Vector((wall_thick * 0.5, half_l + wall_thick * 0.5, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer
            )
            # Inner corner column (+X, -Y corner)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.45, 0.45, h)),
                offset=mathutils.Vector((half_w - 0.225, -half_l + 0.225, h * 0.5)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer
            )

        elif config.corridor_type == "t_junction":
            # Left wall solid
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, l, h)),
                offset=mathutils.Vector((-half_w - wall_thick * 0.5, 0.0, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer
            )
            # Right wall split by branch opening of width w
            branch_seg_l = max(0.4, (l - w) * 0.5)
            # Seg 1 (-Y side)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, branch_seg_l, h)),
                offset=mathutils.Vector((half_w + wall_thick * 0.5, -half_l + branch_seg_l * 0.5, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer
            )
            # Seg 2 (+Y side)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, branch_seg_l, h)),
                offset=mathutils.Vector((half_w + wall_thick * 0.5, half_l - branch_seg_l * 0.5, h * 0.5)),
                mat_idx=m_wall,
                uv_layer=uv_layer,
                uv_rect=r_wall,
                color_layer=color_layer
            )
            # Lintel above branch
            lintel_h = max(0.3, h - config.doorway_height)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((wall_thick, w, lintel_h)),
                offset=mathutils.Vector((half_w + wall_thick * 0.5, 0.0, h - lintel_h * 0.5)),
                mat_idx=m_door_frame,
                uv_layer=uv_layer,
                uv_rect=r_door_frame,
                color_layer=color_layer
            )

        elif config.corridor_type == "cross_junction":
            # 4 corner column assemblies
            col_size = 0.40
            for cx in [-half_w - wall_thick * 0.5, half_w + wall_thick * 0.5]:
                for cy in [-half_l - wall_thick * 0.5, half_l + wall_thick * 0.5]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((col_size, col_size, h)),
                        offset=mathutils.Vector((cx, cy, h * 0.5)),
                        mat_idx=m_beam,
                        uv_layer=uv_layer,
                        uv_rect=r_beam,
                        color_layer=color_layer
                    )

        # Overhead Cable Conduit Raceways
        if config.has_cable_runs and config.corridor_type in ["straight", "doorway_arch", "dead_end"]:
            conduit_size = mathutils.Vector((0.08, l, 0.12))
            MeshBuilder.add_box(
                bm,
                size=conduit_size,
                offset=mathutils.Vector((-half_w + 0.04, 0.0, h - 0.25)),
                mat_idx=m_rubber,
                uv_layer=uv_layer,
                uv_rect=r_rubber,
                color_layer=color_layer,
                rgba=(0.10, 0.10, 0.11, 1.0)
            )

        # Damage: Breached vent
        if config.damage_state == "breached_vent":
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.14, 0.65, 0.65)),
                offset=mathutils.Vector((-half_w + 0.05, 0.0, 0.85)),
                mat_idx=m_grate,
                uv_layer=uv_layer,
                uv_rect=r_grate,
                color_layer=color_layer,
                rgba=(0.12, 0.12, 0.14, 1.0)
            )

        # -------------------------------------------------------------
        # 3. CEILING GENERATION
        # -------------------------------------------------------------
        ceil_thickness = 0.08
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, l, ceil_thickness)),
            offset=mathutils.Vector((0.0, 0.0, h + ceil_thickness * 0.5)),
            mat_idx=m_wall,
            uv_layer=uv_layer,
            uv_rect=r_wall,
            color_layer=color_layer,
            rgba=(0.22, 0.23, 0.25, 1.0)
        )

        # Transverse I-Beams / Girders
        if config.ceiling_style == "exposed_beams":
            beam_count = 2 if l < 4.5 else 3
            for i in range(beam_count):
                fraction = (i + 1) / (beam_count + 1)
                y_pos = -half_l + l * fraction
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((w, 0.18, 0.15)),
                    offset=mathutils.Vector((0.0, y_pos, h - 0.075)),
                    mat_idx=m_girder,
                    uv_layer=uv_layer,
                    uv_rect=r_girder,
                    color_layer=color_layer,
                    rgba=(0.32, 0.35, 0.38, 1.0)
                )

        # Integrated Lighting Fixture
        if config.has_integrated_lighting:
            troffer_l = min(1.8, l * 0.5)
            # Luminaire casing
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.36, troffer_l, 0.08)),
                offset=mathutils.Vector((0.0, 0.0, h - 0.04)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer,
                rgba=(0.20, 0.22, 0.24, 1.0)
            )
            # Fluorescent tube face
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.18, troffer_l * 0.88, 0.02)),
                offset=mathutils.Vector((0.0, 0.0, h - 0.075)),
                mat_idx=m_light,
                uv_layer=uv_layer,
                uv_rect=r_light,
                color_layer=color_layer,
                rgba=(0.95, 0.98, 1.00, 1.0)
            )

        # Damage: Collapsed ceiling panel & dangling wire
        if config.damage_state == "collapsed_ceiling_wires":
            # Loose hanging panel
            panel_pts = [
                mathutils.Vector((-0.4, 0.2, h - 0.05)),
                mathutils.Vector((0.4, 0.2, h - 0.05)),
                mathutils.Vector((0.4, -0.6, h - 0.55)),
                mathutils.Vector((-0.4, -0.6, h - 0.55))
            ]
            panel_face = bm.faces.new([bm.verts.new(p) for p in panel_pts])
            MeshBuilder.apply_face_attributes(panel_face, m_wall, (0.3, 0.3, 0.3, 1.0), color_layer)
            MeshBuilder.apply_face_uv_rect(panel_face, uv_layer, r_wall)

            # Dangling wire
            wire_pts = [
                mathutils.Vector((0.15, -0.5, h - 0.05)),
                mathutils.Vector((0.18, -0.45, h - 0.6)),
                mathutils.Vector((0.12, -0.48, h - 1.15))
            ]
            MeshBuilder.add_extruded_cable(
                bm,
                points=wire_pts,
                radius=0.012,
                sides=4,
                mat_idx=m_rubber,
                rgba=(0.08, 0.08, 0.09, 1.0),
                color_layer=color_layer,
                uv_layer=uv_layer,
                uv_rect=r_rubber
            )

        # -------------------------------------------------------------
        # 4. COMPUTE CONNECTION SOCKETS FOR GODOT 4
        # -------------------------------------------------------------
        sockets: List[Dict[str, Any]] = []
        if config.corridor_type in ["straight", "doorway_arch", "dead_end", "t_junction", "cross_junction"]:
            sockets.append({
                "name": "socket_south",
                "pos": [0.0, round(-half_l, 4), 0.0],
                "forward": [0.0, -1.0, 0.0],
                "width": round(w, 3),
                "height": round(h, 3)
            })

        if config.corridor_type in ["straight", "doorway_arch", "t_junction", "cross_junction"]:
            sockets.append({
                "name": "socket_north",
                "pos": [0.0, round(half_l, 4), 0.0],
                "forward": [0.0, 1.0, 0.0],
                "width": round(w, 3),
                "height": round(h, 3)
            })

        if config.corridor_type in ["corner_90", "t_junction", "cross_junction"]:
            sockets.append({
                "name": "socket_east",
                "pos": [round(half_w, 4), 0.0, 0.0],
                "forward": [1.0, 0.0, 0.0],
                "width": round(w, 3),
                "height": round(h, 3)
            })

        if config.corridor_type == "cross_junction":
            sockets.append({
                "name": "socket_west",
                "pos": [round(-half_w, 4), 0.0, 0.0],
                "forward": [-1.0, 0.0, 0.0],
                "width": round(w, 3),
                "height": round(h, 3)
            })

        config.connection_sockets = sockets

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: StationCorridorConfig) -> ValidationReport:
        report = super().validate(obj, config)
        if len(config.connection_sockets) == 0:
            report.warnings.append("Corridor generated with 0 connection sockets.")
        return report
