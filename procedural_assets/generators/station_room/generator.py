import math
import mathutils
import bmesh
import bpy
from typing import List, Dict, Any

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import StationRoomConfig

class StationRoomGenerator(BaseAssetGenerator):
    """Procedural generator for modular space station rooms and chambers."""

    def generate(self, config: StationRoomConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        w = config.width
        d = config.depth
        h = config.height
        half_w = w * 0.5
        half_d = d * 0.5

        # Archetype adjustments
        has_window = config.has_observation_window or (config.room_archetype == "control_hub")
        has_gantry = config.has_overhead_gantry or (config.room_archetype == "cargo_bay")
        has_drain = config.has_floor_drain or (config.room_archetype == "medbay_lab")
        elevation = config.floor_elevation
        if config.room_archetype == "control_hub" and elevation == "flat":
            elevation = "raised_platform"

        # Material indices & UV rects
        m_floor = mat_mgr.get_index("floor_metal")
        r_floor = mat_mgr.get_rect("floor_metal")

        m_hazard = mat_mgr.get_index("floor_hazard")
        r_hazard = mat_mgr.get_rect("hazard_yellow")

        m_grate = mat_mgr.get_index("floor_grate")
        r_grate = mat_mgr.get_rect("vent")

        m_wall = mat_mgr.get_index("wall_bulkhead")
        r_wall = mat_mgr.get_rect("metal_dark_grime")

        m_beam = mat_mgr.get_index("wall_support_beam")
        r_beam = mat_mgr.get_rect("metal_light_brushed")

        m_girder = mat_mgr.get_index("ceiling_girder")
        r_girder = mat_mgr.get_rect("metal_light_brushed")

        m_door_frame = mat_mgr.get_index("door_emergency_red")
        r_door_frame = mat_mgr.get_rect("door_emergency_red")

        m_glass = mat_mgr.get_index("glass_observation")
        r_glass = mat_mgr.get_rect("glass_observation")

        # Emissive lighting
        m_light = mat_mgr.get_index("fluorescent_tube_lit")
        r_light = mat_mgr.get_rect("fluorescent_lit")
        if config.lighting_color == "emergency_red":
            m_light = mat_mgr.get_index("led_red")
            r_light = mat_mgr.get_rect("led_red")
        elif config.lighting_color == "medbay_cyan":
            m_light = mat_mgr.get_index("oxygen_cyan")
            r_light = mat_mgr.get_rect("oxygen_cyan")
        elif config.lighting_color == "dim_amber":
            m_light = mat_mgr.get_index("memory_cartridge")
            r_light = mat_mgr.get_rect("cartridge_amber")

        # -------------------------------------------------------------
        # 1. FLOOR & PLATFORMS
        # -------------------------------------------------------------
        floor_thick = 0.08
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, d, floor_thick)),
            offset=mathutils.Vector((0.0, 0.0, -floor_thick * 0.5)),
            mat_idx=m_floor,
            uv_layer=uv_layer,
            uv_rect=r_floor,
            color_layer=color_layer,
            rgba=(0.24, 0.26, 0.28, 1.0)
        )

        # Floor drainage trench
        if has_drain:
            trench_w = min(1.2, w * 0.25)
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((trench_w, d * 0.75, 0.006)),
                offset=mathutils.Vector((0.0, 0.0, 0.003)),
                mat_idx=m_grate,
                uv_layer=uv_layer,
                uv_rect=r_grate,
                color_layer=color_layer,
                rgba=(0.20, 0.20, 0.22, 1.0)
            )

        # Raised command platform
        if elevation == "raised_platform":
            plat_d = d * 0.38
            plat_h = 0.35
            plat_y = half_d - plat_d * 0.5
            # Platform slab
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.88, plat_d, plat_h)),
                offset=mathutils.Vector((0.0, plat_y, plat_h * 0.5)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer,
                rgba=(0.32, 0.35, 0.38, 1.0)
            )
            # Front step stair
            step_d = 0.35
            step_h = plat_h * 0.5
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w * 0.60, step_d, step_h)),
                offset=mathutils.Vector((0.0, half_d - plat_d - step_d * 0.5, step_h * 0.5)),
                mat_idx=m_hazard,
                uv_layer=uv_layer,
                uv_rect=r_hazard,
                color_layer=color_layer,
                rgba=(0.85, 0.65, 0.10, 1.0)
            )

        # Sunken pit
        elif elevation == "sunken_pit":
            pit_w = w * 0.55
            pit_d = d * 0.55
            curb_w = 0.20
            curb_h = 0.22
            # Perimeter curbing
            for sign_x in [-1, 1]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((curb_w, pit_d + curb_w * 2.0, curb_h)),
                    offset=mathutils.Vector((sign_x * (pit_w * 0.5 + curb_w * 0.5), 0.0, curb_h * 0.5)),
                    mat_idx=m_hazard,
                    uv_layer=uv_layer,
                    uv_rect=r_hazard,
                    color_layer=color_layer
                )

        # Perimeter floor hazard stripes
        stripe_w = 0.25
        for sx in [-half_w + stripe_w * 0.5, half_w - stripe_w * 0.5]:
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((stripe_w, d, 0.005)),
                offset=mathutils.Vector((sx, 0.0, 0.002)),
                mat_idx=m_hazard,
                uv_layer=uv_layer,
                uv_rect=r_hazard,
                color_layer=color_layer,
                rgba=(0.85, 0.65, 0.10, 1.0)
            )

        # -------------------------------------------------------------
        # 2. WALLS WITH DOORWAYS AND OBSERVATION VIEWPORT
        # -------------------------------------------------------------
        wall_thick = 0.20
        dw = config.doorway_width
        dh = config.doorway_height

        def build_wall_with_optional_door(length: float, has_door: bool, is_ns: bool, pos_offset: float, is_north: bool = False):
            """Builds either a solid wall or a 3-part wall with a door opening in the center."""
            if has_door:
                seg_len = max(0.4, (length - dw) * 0.5)
                lintel_h = max(0.2, h - dh)

                if is_ns:
                    # Wall runs along X at Y = pos_offset
                    # Left segment (-X)
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((seg_len, wall_thick, h)),
                        offset=mathutils.Vector((-length * 0.5 + seg_len * 0.5, pos_offset, h * 0.5)),
                        mat_idx=m_wall,
                        uv_layer=uv_layer,
                        uv_rect=r_wall,
                        color_layer=color_layer
                    )
                    # Right segment (+X)
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((seg_len, wall_thick, h)),
                        offset=mathutils.Vector((length * 0.5 - seg_len * 0.5, pos_offset, h * 0.5)),
                        mat_idx=m_wall,
                        uv_layer=uv_layer,
                        uv_rect=r_wall,
                        color_layer=color_layer
                    )
                    # Lintel header above door
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((dw, wall_thick, lintel_h)),
                        offset=mathutils.Vector((0.0, pos_offset, dh + lintel_h * 0.5)),
                        mat_idx=m_door_frame,
                        uv_layer=uv_layer,
                        uv_rect=r_door_frame,
                        color_layer=color_layer
                    )
                else:
                    # Wall runs along Y at X = pos_offset
                    # Seg 1 (-Y)
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((wall_thick, seg_len, h)),
                        offset=mathutils.Vector((pos_offset, -length * 0.5 + seg_len * 0.5, h * 0.5)),
                        mat_idx=m_wall,
                        uv_layer=uv_layer,
                        uv_rect=r_wall,
                        color_layer=color_layer
                    )
                    # Seg 2 (+Y)
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((wall_thick, seg_len, h)),
                        offset=mathutils.Vector((pos_offset, length * 0.5 - seg_len * 0.5, h * 0.5)),
                        mat_idx=m_wall,
                        uv_layer=uv_layer,
                        uv_rect=r_wall,
                        color_layer=color_layer
                    )
                    # Lintel header
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((wall_thick, dw, lintel_h)),
                        offset=mathutils.Vector((pos_offset, 0.0, dh + lintel_h * 0.5)),
                        mat_idx=m_door_frame,
                        uv_layer=uv_layer,
                        uv_rect=r_door_frame,
                        color_layer=color_layer
                    )
            else:
                # Solid wall or Observation Viewport
                if is_ns:
                    if is_north and has_window:
                        # Observation Viewport Window on North wall
                        win_w = w * 0.65
                        win_h = 1.40
                        sill_h = 1.00
                        side_w = (w - win_w) * 0.5
                        # Left side wall
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((side_w, wall_thick, h)),
                            offset=mathutils.Vector((-half_w + side_w * 0.5, pos_offset, h * 0.5)),
                            mat_idx=m_wall,
                            uv_layer=uv_layer,
                            uv_rect=r_wall,
                            color_layer=color_layer
                        )
                        # Right side wall
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((side_w, wall_thick, h)),
                            offset=mathutils.Vector((half_w - side_w * 0.5, pos_offset, h * 0.5)),
                            mat_idx=m_wall,
                            uv_layer=uv_layer,
                            uv_rect=r_wall,
                            color_layer=color_layer
                        )
                        # Sill bottom wall
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((win_w, wall_thick, sill_h)),
                            offset=mathutils.Vector((0.0, pos_offset, sill_h * 0.5)),
                            mat_idx=m_beam,
                            uv_layer=uv_layer,
                            uv_rect=r_beam,
                            color_layer=color_layer
                        )
                        # Top header wall
                        top_h = h - (sill_h + win_h)
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((win_w, wall_thick, top_h)),
                            offset=mathutils.Vector((0.0, pos_offset, h - top_h * 0.5)),
                            mat_idx=m_beam,
                            uv_layer=uv_layer,
                            uv_rect=r_beam,
                            color_layer=color_layer
                        )
                        # Glass pane
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((win_w * 0.95, 0.04, win_h * 0.95)),
                            offset=mathutils.Vector((0.0, pos_offset, sill_h + win_h * 0.5)),
                            mat_idx=m_glass,
                            uv_layer=uv_layer,
                            uv_rect=r_glass,
                            color_layer=color_layer,
                            rgba=(0.05, 0.10, 0.15, 0.85)
                        )
                    else:
                        MeshBuilder.add_box(
                            bm,
                            size=mathutils.Vector((length, wall_thick, h)),
                            offset=mathutils.Vector((0.0, pos_offset, h * 0.5)),
                            mat_idx=m_wall,
                            uv_layer=uv_layer,
                            uv_rect=r_wall,
                            color_layer=color_layer
                        )
                else:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((wall_thick, length, h)),
                        offset=mathutils.Vector((pos_offset, 0.0, h * 0.5)),
                        mat_idx=m_wall,
                        uv_layer=uv_layer,
                        uv_rect=r_wall,
                        color_layer=color_layer
                    )

        # North (+Y)
        build_wall_with_optional_door(length=w, has_door=config.door_north, is_ns=True, pos_offset=half_d + wall_thick * 0.5, is_north=True)
        # South (-Y)
        build_wall_with_optional_door(length=w, has_door=config.door_south, is_ns=True, pos_offset=-half_d - wall_thick * 0.5)
        # East (+X)
        build_wall_with_optional_door(length=d, has_door=config.door_east, is_ns=False, pos_offset=half_w + wall_thick * 0.5)
        # West (-X)
        build_wall_with_optional_door(length=d, has_door=config.door_west, is_ns=False, pos_offset=-half_w - wall_thick * 0.5)

        # -------------------------------------------------------------
        # 3. COLUMNS & STRUCTURAL BUTTRESSES
        # -------------------------------------------------------------
        if config.pillar_layout == "center_single":
            col_size = 0.65
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((col_size, col_size, h)),
                offset=mathutils.Vector((0.0, 0.0, h * 0.5)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer
            )
        elif config.pillar_layout == "dual_columns":
            col_size = 0.55
            for col_y in [-d * 0.22, d * 0.22]:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((col_size, col_size, h)),
                    offset=mathutils.Vector((0.0, col_y, h * 0.5)),
                    mat_idx=m_beam,
                    uv_layer=uv_layer,
                    uv_rect=r_beam,
                    color_layer=color_layer
                )
        elif config.pillar_layout == "perimeter_buttresses":
            butt_w = 0.35
            butt_d = 0.35
            for bx in [-half_w + butt_w * 0.5, half_w - butt_w * 0.5]:
                for by in [-half_d + butt_d * 0.5, half_d - butt_d * 0.5]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((butt_w, butt_d, h)),
                        offset=mathutils.Vector((bx, by, h * 0.5)),
                        mat_idx=m_beam,
                        uv_layer=uv_layer,
                        uv_rect=r_beam,
                        color_layer=color_layer
                    )

        # -------------------------------------------------------------
        # 4. CEILING, GIRDERS, CRANE GANTRY & LIGHTING
        # -------------------------------------------------------------
        ceil_thick = 0.08
        MeshBuilder.add_box(
            bm,
            size=mathutils.Vector((w, d, ceil_thick)),
            offset=mathutils.Vector((0.0, 0.0, h + ceil_thick * 0.5)),
            mat_idx=m_wall,
            uv_layer=uv_layer,
            uv_rect=r_wall,
            color_layer=color_layer
        )

        # Ceiling support girders spanning across X
        girder_count = 3 if d > 7.0 else 2
        for i in range(girder_count):
            frac = (i + 1) / (girder_count + 1)
            gy = -half_d + d * frac
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, 0.22, 0.18)),
                offset=mathutils.Vector((0.0, gy, h - 0.09)),
                mat_idx=m_girder,
                uv_layer=uv_layer,
                uv_rect=r_girder,
                color_layer=color_layer
            )

        # Overhead Industrial Crane Gantry
        if has_gantry:
            gantry_beam_w = 0.30
            gantry_beam_h = 0.25
            # Longitudinal beam along Y
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((gantry_beam_w, d, gantry_beam_h)),
                offset=mathutils.Vector((0.0, 0.0, h - 0.28)),
                mat_idx=m_hazard,
                uv_layer=uv_layer,
                uv_rect=r_hazard,
                color_layer=color_layer
            )
            # Crane Hoist Trolley
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.55, 0.55, 0.22)),
                offset=mathutils.Vector((0.0, 0.0, h - 0.48)),
                mat_idx=m_beam,
                uv_layer=uv_layer,
                uv_rect=r_beam,
                color_layer=color_layer
            )

        # Lighting Troffers
        light_rows = 2
        for lx in [-w * 0.25, w * 0.25]:
            for ly in [-d * 0.25, d * 0.25]:
                # Casing
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.35, 1.2, 0.08)),
                    offset=mathutils.Vector((lx, ly, h - 0.04)),
                    mat_idx=m_beam,
                    uv_layer=uv_layer,
                    uv_rect=r_beam,
                    color_layer=color_layer
                )
                # Emissive tube
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((0.18, 1.05, 0.02)),
                    offset=mathutils.Vector((lx, ly, h - 0.075)),
                    mat_idx=m_light,
                    uv_layer=uv_layer,
                    uv_rect=r_light,
                    color_layer=color_layer
                )

        # -------------------------------------------------------------
        # 5. COMPUTE DOORWAY SOCKETS FOR GODOT 4
        # -------------------------------------------------------------
        sockets: List[Dict[str, Any]] = []
        if config.door_north:
            sockets.append({
                "name": "door_north",
                "pos": [0.0, round(half_d, 4), 0.0],
                "forward": [0.0, 1.0, 0.0],
                "width": round(dw, 3),
                "height": round(dh, 3)
            })
        if config.door_south:
            sockets.append({
                "name": "door_south",
                "pos": [0.0, round(-half_d, 4), 0.0],
                "forward": [0.0, -1.0, 0.0],
                "width": round(dw, 3),
                "height": round(dh, 3)
            })
        if config.door_east:
            sockets.append({
                "name": "door_east",
                "pos": [round(half_w, 4), 0.0, 0.0],
                "forward": [1.0, 0.0, 0.0],
                "width": round(dw, 3),
                "height": round(dh, 3)
            })
        if config.door_west:
            sockets.append({
                "name": "door_west",
                "pos": [round(-half_w, 4), 0.0, 0.0],
                "forward": [-1.0, 0.0, 0.0],
                "width": round(dw, 3),
                "height": round(dh, 3)
            })

        config.doorway_sockets = sockets

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: StationRoomConfig) -> ValidationReport:
        report = super().validate(obj, config)
        return report
