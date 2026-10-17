import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from ...core.transform_utils import generate_catenary_cable_points
from .config import OxypodConfig

class OxypodGenerator(BaseAssetGenerator[OxypodConfig]):
    """Procedural generator for Oxypod oxygen recovery stations and canisters (PSX aesthetic)."""

    def generate(self, config: OxypodConfig) -> bpy.types.Object:
        self.clean_context()
        rng = random.Random(config.seed)

        self.material_manager = self.get_material_manager(config)
        mesh_name = f"{config.name}_mesh"
        obj_name = config.name

        if obj_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)
        if mesh_name in bpy.data.meshes:
            bpy.data.meshes.remove(bpy.data.meshes[mesh_name], do_unlink=True)

        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)

        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices
        rgba = {k: self.material_manager.get_rgba(k) for k in self.material_manager.palette.keys()}

        bm = bmesh.new()
        col_layer = bm.loops.layers.color.new("Color")

        tank_rad = config.tank_radius
        tank_h = config.tank_height
        tank_z = tank_rad + 0.05

        # Fluid color based on level
        if config.oxygen_level > 0.4:
            fluid_mat = "oxygen_cyan"
        elif config.oxygen_level > 0.15:
            fluid_mat = "led_yellow"
        else:
            fluid_mat = "led_red"

        # 1. Mount / Base Structure
        if config.station_type == "wall_station":
            plate_w = tank_rad * 2.6
            plate_h = tank_h * 1.12
            plate_d = 0.03
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((plate_w, plate_h, plate_d)),
                offset=mathutils.Vector((0.0, 0.0, plate_d / 2.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
                color_layer=col_layer
            )
            # Retaining collar clamps
            for clamp_y in (tank_h * 0.3, -tank_h * 0.3):
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((plate_w * 0.9, 0.04, tank_z)),
                    offset=mathutils.Vector((0.0, clamp_y, tank_z / 2.0)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.3, 0.3, 0.3, 1.0)),
                    color_layer=col_layer
                )
        elif config.station_type == "portable_canister":
            # Top Carry Handle (U-bar)
            handle_y = (tank_h / 2.0) + 0.12
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((tank_rad * 1.4, 0.03, 0.03)),
                offset=mathutils.Vector((0.0, handle_y, tank_z)),
                mat_idx=m_idx.get("screw", 0),
                rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer
            )
            for hx in (-tank_rad * 0.6, tank_rad * 0.6):
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.025, 0.12, 0.025)),
                    offset=mathutils.Vector((hx, handle_y - 0.06, tank_z)),
                    mat_idx=m_idx.get("screw", 0),
                    rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer
                )
            # Skid ring feet at bottom
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=tank_rad * 1.15,
                depth=0.03,
                segments=6,
                offset=mathutils.Vector((0.0, -(tank_h / 2.0) - 0.015, tank_z)),
                axis='Y',
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 2. Main High-Pressure Oxygen Tank(s)
        tank_positions = [mathutils.Vector((0.0, 0.0, tank_z))]
        if config.station_type == "dual_tank_rig":
            tank_offset_x = tank_rad * 1.1
            tank_positions = [
                mathutils.Vector((-tank_offset_x, 0.0, tank_z)),
                mathutils.Vector((tank_offset_x, 0.0, tank_z))
            ]
            # Link manifold cross tube
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.03,
                depth=tank_offset_x * 2.2,
                segments=5,
                offset=mathutils.Vector((0.0, tank_h * 0.4, tank_z)),
                axis='X',
                mat_idx=m_idx.get("pipe_industrial", 0),
                rgba=rgba.get("pipe_industrial", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        for pos in tank_positions:
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=tank_rad,
                depth=tank_h,
                segments=6,
                offset=pos,
                axis='Y',
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.3, 0.35, 0.38, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            # Reinforcing collar bands
            for cap_y in (tank_h / 2.0, -tank_h / 2.0):
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=tank_rad * 1.08,
                    depth=0.04,
                    segments=6,
                    offset=mathutils.Vector((pos.x, cap_y, pos.z)),
                    axis='Y',
                    mat_idx=m_idx.get("hazard_yellow", 0),
                    rgba=rgba.get("hazard_yellow", (0.8, 0.6, 0.1, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

        # 3. Glowing Oxygen Sight Gauge
        if config.has_gauge_sight:
            primary_tank_x = tank_positions[0].x
            gauge_w = 0.04
            gauge_h = tank_h * 0.55
            gauge_d = 0.02
            gauge_pos = mathutils.Vector((primary_tank_x, 0.0, tank_z + tank_rad - 0.005))

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((gauge_w + 0.02, gauge_h + 0.02, gauge_d)),
                offset=gauge_pos,
                mat_idx=m_idx.get("glass_tube", 0),
                rgba=rgba.get("glass_tube", (0.2, 0.3, 0.4, 1.0)),
                color_layer=col_layer
            )
            # Glowing fluid
            clamped_level = max(0.05, min(1.0, config.oxygen_level))
            fluid_h = gauge_h * clamped_level
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((gauge_w, fluid_h, gauge_d + 0.005)),
                offset=mathutils.Vector((primary_tank_x, -(gauge_h * (1.0 - clamped_level) / 2.0), gauge_pos.z + 0.002)),
                mat_idx=m_idx.get(fluid_mat, 0),
                rgba=rgba.get(fluid_mat, (0.1, 0.9, 0.95, 1.0)),
                color_layer=col_layer
            )

        # 4. Pressure Gauges
        top_gauge_y = (tank_h / 2.0) + 0.06
        top_pos = mathutils.Vector((tank_positions[0].x, top_gauge_y, tank_z))
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=0.065,
            depth=0.03,
            segments=6,
            offset=top_pos,
            axis='Z',
            mat_idx=m_idx.get("screw", 0),
            rgba=rgba.get("screw", (0.35, 0.35, 0.35, 1.0)),
            color_layer=col_layer,
            smooth=False
        )

        if config.has_dual_gauges and len(tank_positions) > 1:
            top_pos2 = mathutils.Vector((tank_positions[1].x, top_gauge_y, tank_z))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.065,
                depth=0.03,
                segments=6,
                offset=top_pos2,
                axis='Z',
                mat_idx=m_idx.get("screw", 0),
                rgba=rgba.get("screw", (0.35, 0.35, 0.35, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 5. Breathing Mask Dock & Hanging Hose
        if config.has_mask_dock:
            dock_x = tank_positions[-1].x + tank_rad + 0.04
            dock_pos = mathutils.Vector((dock_x, -tank_h * 0.22, tank_z))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.04,
                depth=0.05,
                segments=5,
                offset=dock_pos,
                axis='X',
                mat_idx=m_idx.get("switch_base", 0),
                rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

            # Hanging flexible breathing hose
            if config.has_coiled_hose:
                hose_start = mathutils.Vector((dock_x + 0.02, dock_pos.y, dock_pos.z))
                hose_end = mathutils.Vector((dock_x - 0.05, dock_pos.y - 0.45, dock_pos.z + 0.05))
                hose_pts = generate_catenary_cable_points(hose_start, hose_end, segments=5, sag=0.12)
                MeshBuilder.add_extruded_cable(
                    bm=bm,
                    points=hose_pts,
                    radius=0.012,
                    sides=3,
                    mat_idx=m_idx.get("cable_hazard", 0),
                    rgba=rgba.get("cable_hazard", (0.8, 0.6, 0.1, 1.0)),
                    color_layer=col_layer
                )

        # 6. Status Dome Beacon
        if config.beacon_state != "off":
            beacon_color = "oxygen_cyan" if config.beacon_state == "cyan" else ("led_green" if config.beacon_state == "green" else "led_red")
            beacon_pos = mathutils.Vector((0.0, top_gauge_y + 0.065, tank_z))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.035,
                depth=0.045,
                segments=4,
                offset=beacon_pos,
                axis='Y',
                mat_idx=m_idx.get(beacon_color, 0),
                rgba=rgba.get(beacon_color, (0.1, 0.9, 0.9, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        bmesh.ops.rotate(
            bm,
            cent=(0.0, 0.0, 0.0),
            matrix=mathutils.Matrix.Rotation(math.radians(90.0), 3, 'X'),
            verts=bm.verts
        )
        min_z = min(v.co.z for v in bm.verts)
        bmesh.ops.translate(
            bm,
            vec=(0.0, 0.0, -min_z),
            verts=bm.verts
        )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

