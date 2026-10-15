import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ElectricalPanelConfig
from .components.casing import CasingComponent
from .components.fasteners import FastenersComponent
from .components.crt import CRTComponent
from .components.controls import ControlsComponent
from .components.indicators import IndicatorsComponent
from .components.cables import CablesComponent

class ElectricalPanelGenerator(BaseAssetGenerator[ElectricalPanelConfig]):
    """Procedural generator for industrial electrical panels (PSX low-poly aesthetic)."""

    def __init__(self, material_manager: Optional[MaterialManager] = None):
        super().__init__(material_manager)

    def generate(self, config: ElectricalPanelConfig) -> bpy.types.Object:
        """Procedurally generate complete electrical panel geometry."""
        self.clean_context()

        # Seeded deterministic RNG
        rng = random.Random(config.seed)

        # 1. Prepare material manager and scene object
        self.material_manager = self.get_material_manager(config)
        mesh_name = f"{config.name}_mesh"
        obj_name = config.name

        # Clean existing meshes/objects with same name
        if obj_name in bpy.data.objects:
            old_obj = bpy.data.objects[obj_name]
            bpy.data.objects.remove(old_obj, do_unlink=True)
        if mesh_name in bpy.data.meshes:
            old_mesh = bpy.data.meshes[mesh_name]
            bpy.data.meshes.remove(old_mesh, do_unlink=True)

        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)

        # Assign material slots
        self.material_manager.assign_to_mesh(obj)
        mat_indices = self.material_manager.material_indices
        rgba_map = {k: self.material_manager.get_rgba(k) for k in self.material_manager.palette.keys()}

        # 2. Budget-adaptive resolution allocation
        budget = config.target_tri_budget
        if budget < 320:
            bolt_sides = 4
            add_side_bolts = False
            control_sides = 4
            indicator_sides = 3
            cable_sides = 3
            cable_segments = 3
            vent_count = 0
        elif budget < 440:
            bolt_sides = 4
            add_side_bolts = False
            control_sides = 4
            indicator_sides = 4
            cable_sides = 3
            cable_segments = 3
            vent_count = 0
        elif budget < 550:
            bolt_sides = 4
            add_side_bolts = False
            control_sides = 4
            indicator_sides = 4
            cable_sides = 3
            cable_segments = 4
            vent_count = 1 if config.has_side_vents else 0
        elif budget < 700:
            bolt_sides = 5
            add_side_bolts = False
            control_sides = 5
            indicator_sides = 5
            cable_sides = 4
            cable_segments = 4
            vent_count = 2 if config.has_side_vents else 0
        else:
            bolt_sides = 6
            add_side_bolts = True
            control_sides = 6
            indicator_sides = 6
            cable_sides = 4
            cable_segments = 5
            vent_count = 3 if config.has_side_vents else 0

        # 3. Create BMesh and attribute layers
        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Color")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        # 4. Enclosure Casing
        CasingComponent.build(
            bm=bm,
            width=config.width,
            height=config.height,
            depth=config.depth,
            wall_thickness=config.wall_thickness,
            has_mounting_flanges=config.has_mounting_flanges,
            has_side_vents=config.has_side_vents,
            vent_count=vent_count,
            mat_indices=mat_indices,
            color_layer=color_layer,
            rgba_map=rgba_map
        )

        # 5. Fasteners / Corner Screws
        FastenersComponent.build(
            bm=bm,
            width=config.width,
            height=config.height,
            depth=config.depth,
            margin=config.wall_thickness * 0.7,
            sides=bolt_sides,
            add_side_bolts=add_side_bolts,
            mat_indices=mat_indices,
            color_layer=color_layer,
            rgba_map=rgba_map
        )

        # 6. Front panel layout partitioning
        # Inner plate sits at Z = depth
        front_z = config.depth + 0.002
        usable_w = config.width - (2.0 * config.wall_thickness) - 0.04
        usable_h = config.height - (2.0 * config.wall_thickness) - 0.04

        upper_ratio = config.crt_size_ratio if config.has_crt else 0.32
        upper_h = usable_h * upper_ratio
        lower_h = usable_h * 0.18
        middle_h = usable_h - upper_h - lower_h

        # Y-centers of regions (relative to center 0,0)
        upper_y = (usable_h / 2.0) - (upper_h / 2.0)
        lower_y = -(usable_h / 2.0) + (lower_h / 2.0)
        middle_y = lower_y + (lower_h / 2.0) + (middle_h / 2.0)

        # --- UPPER SECTION: CRT Screen or Analog Gauges ---
        if config.has_crt:
            screen_w = min(usable_w * 0.85, upper_h * 1.35)
            screen_h = min(upper_h * 0.75, usable_w * 0.65)
            crt_center = mathutils.Vector((0.0, upper_y, front_z))
            CRTComponent.build(
                bm=bm,
                screen_w=screen_w,
                screen_h=screen_h,
                bulge=config.crt_bulge,
                center_pos=crt_center,
                phosphor_color=config.crt_phosphor_color,
                mat_indices=mat_indices,
                color_layer=color_layer,
                rgba_map=rgba_map
            )
        else:
            # Dual analog gauges instead of CRT
            gauge_rad = min(usable_w * 0.22, upper_h * 0.38)
            gauge_spacing = usable_w * 0.45
            for side in (-1, 1):
                gauge_pos = mathutils.Vector((side * (gauge_spacing / 2.0), upper_y, front_z))
                IndicatorsComponent.add_analog_gauge(
                    bm=bm,
                    pos=gauge_pos,
                    radius=gauge_rad,
                    sides=control_sides,
                    mat_indices=mat_indices,
                    color_layer=color_layer,
                    rgba_map=rgba_map
                )

        # --- MIDDLE SECTION: Controls & Indicator LEDs ---
        # Status LED strip at top of middle region
        led_y = middle_y + (middle_h / 2.0) - 0.035
        if config.indicator_count > 0:
            led_spacing = min(usable_w / max(1, config.indicator_count), 0.055)
            led_start_x = -((config.indicator_count - 1) * led_spacing) / 2.0
            IndicatorsComponent.build_strip(
                bm=bm,
                start_pos=mathutils.Vector((led_start_x, led_y, front_z)),
                count=config.indicator_count,
                spacing=led_spacing,
                sides=indicator_sides,
                rng=rng,
                mat_indices=mat_indices,
                color_layer=color_layer,
                rgba_map=rgba_map
            )

        # Digital LED Segment Readout (Right beside LED strip)
        if config.has_digital_readout:
            readout_x = (usable_w / 2.0) - 0.06
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.08, 0.03, 0.015)),
                offset=mathutils.Vector((readout_x, led_y, front_z + 0.01)),
                mat_idx=mat_indices.get("led_green", 0),
                rgba=rgba_map.get("led_green", (0.1, 0.9, 0.2, 1.0)),
                color_layer=color_layer
            )

        # Heavy Industrial Knife Breaker Switch
        if config.has_knife_switch:
            knife_x = -(usable_w / 2.0) + 0.06
            knife_y = middle_y - 0.03
            # Knife switch base block
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.05, 0.12, 0.02)),
                offset=mathutils.Vector((knife_x, knife_y, front_z + 0.01)),
                mat_idx=mat_indices.get("switch_base", 0),
                rgba=rgba_map.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                color_layer=color_layer
            )
            # Tilted copper knife lever
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.015, 0.10, 0.05)),
                offset=mathutils.Vector((knife_x, knife_y + 0.02, front_z + 0.035)),
                mat_idx=mat_indices.get("switch_metal", 0),
                rgba=rgba_map.get("switch_metal", (0.8, 0.5, 0.1, 1.0)),
                color_layer=color_layer
            )

        # Hinged Maintenance Door (Swung open if door_ajar is True)
        if config.door_ajar:
            door_angle = math.radians(config.door_open_angle)
            door_w = config.width * 0.95
            door_h = config.height * 0.95
            hinge_x = -(config.width / 2.0)
            door_center_x = hinge_x - math.cos(door_angle) * (door_w / 2.0)
            door_center_z = front_z + math.sin(door_angle) * (door_w / 2.0)
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((door_w * 0.85, door_h, 0.02)),
                offset=mathutils.Vector((door_center_x, 0.0, door_center_z)),
                mat_idx=mat_indices.get("casing", 0),
                rgba=rgba_map.get("casing", (0.2, 0.2, 0.2, 1.0)),
                color_layer=color_layer,
                uv_layer=uv_layer,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Control grid (buttons, switches, knobs)
        ctrl_h = middle_h - 0.08
        ctrl_y = middle_y - 0.025
        ControlsComponent.build_grid(
            bm=bm,
            center=mathutils.Vector((0.0, ctrl_y, front_z)),
            width=usable_w * 0.88,
            height=ctrl_h,
            rows=config.button_rows,
            cols=config.button_cols,
            switch_count=config.switch_count,
            sides=control_sides,
            rng=rng,
            mat_indices=mat_indices,
            color_layer=color_layer,
            rgba_map=rgba_map
        )

        # --- LOWER SECTION: Hanging Umbilical Cables ---
        bottom_edge_pos = mathutils.Vector((0.0, -(config.height / 2.0), config.depth * 0.5))
        CablesComponent.build(
            bm=bm,
            bottom_pos=bottom_edge_pos,
            count=config.cable_count,
            panel_w=config.width,
            panel_h=config.height,
            cable_sides=cable_sides,
            curve_segments=cable_segments,
            rng=rng,
            mat_indices=mat_indices,
            color_layer=color_layer,
            rgba_map=rgba_map
        )

        # 7. Finalize BMesh and transfer to Blender Mesh
        bm.to_mesh(mesh)
        bm.free()

        mesh.update()
        return obj
