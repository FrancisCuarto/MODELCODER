import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from .config import ServerRackConfig

class ServerRackGenerator(BaseAssetGenerator[ServerRackConfig]):
    """Procedural generator for consciousness storage and server racks (PSX low-poly)."""

    def generate(self, config: ServerRackConfig) -> bpy.types.Object:
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

        rack_w = config.width
        rack_h = config.height
        rack_d = config.depth

        # 1. Outer Cabinet Enclosure
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((rack_w, rack_h, rack_d)),
            offset=mathutils.Vector((0.0, rack_h / 2.0, 0.0)),
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
            color_layer=col_layer
        )

        inner_w = rack_w * 0.85
        inner_h = rack_h * 0.90
        front_z = (rack_d / 2.0) + 0.005

        # 2. Stacked Server Blades
        blade_count = max(3, min(8, config.blade_units))
        blade_h = (inner_h * 0.95) / blade_count
        start_y = (rack_h / 2.0) - (inner_h / 2.0) + (blade_h / 2.0) + 0.03

        for b in range(blade_count):
            by = start_y + (b * blade_h)
            blade_offset = mathutils.Vector((0.0, by, front_z))

            # Check if this blade is the Service Terminal (usually middle blade #2 or #3)
            is_terminal_blade = config.has_service_terminal and (b == 2)

            if is_terminal_blade:
                # 1U Slide-out Service Terminal
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((inner_w, blade_h * 0.88, 0.06)),
                    offset=mathutils.Vector((0.0, by, front_z + 0.015)),
                    mat_idx=m_idx.get("casing_inner", 0),
                    rgba=rgba.get("casing_inner", (0.25, 0.25, 0.25, 1.0)),
                    color_layer=col_layer
                )
                # Miniature CRT display on left
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.14, blade_h * 0.65, 0.02)),
                    offset=mathutils.Vector((-inner_w * 0.25, by, front_z + 0.045)),
                    mat_idx=m_idx.get("crt_screen_green", 0),
                    rgba=rgba.get("crt_screen_green", (0.1, 0.9, 0.3, 1.0)),
                    color_layer=col_layer
                )
                # Miniature keyboard on right
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((inner_w * 0.35, blade_h * 0.55, 0.015)),
                    offset=mathutils.Vector((inner_w * 0.15, by, front_z + 0.045)),
                    mat_idx=m_idx.get("button_gray", 0),
                    rgba=rgba.get("button_gray", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer
                )

            else:
                # Standard Blade Face
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((inner_w, blade_h * 0.88, 0.03)),
                    offset=blade_offset,
                    mat_idx=m_idx.get("server_blade_metal", 0),
                    rgba=rgba.get("server_blade_metal", (0.2, 0.2, 0.2, 1.0)),
                    color_layer=col_layer
                )

                # Consciousness Storage Cartridges
                if config.rack_type == "consciousness_bank":
                    for slot in range(3):
                        if rng.random() <= config.cartridge_occupancy:
                            slot_x = -inner_w * 0.3 + (slot * (inner_w * 0.3))
                            cartridge_pos = mathutils.Vector((slot_x, by, front_z + 0.02))
                            MeshBuilder.add_box(
                                bm=bm,
                                size=mathutils.Vector((0.06, blade_h * 0.55, 0.025)),
                                offset=cartridge_pos,
                                mat_idx=m_idx.get("memory_cartridge", 0),
                                rgba=rgba.get("memory_cartridge", (0.8, 0.5, 0.1, 1.0)),
                                color_layer=col_layer
                            )

            # Activity LEDs on right side
            led_x = (inner_w / 2.0) - 0.04
            led_color = "led_green" if rng.random() > 0.35 else "led_yellow"
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.008,
                depth=0.012,
                segments=4,
                offset=mathutils.Vector((led_x, by, front_z + 0.02)),
                axis='Z',
                mat_idx=m_idx.get(led_color, 0),
                rgba=rgba.get(led_color, (0.2, 0.9, 0.2, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 3. Cooling System (Cryo pipes vs Louvers)
        if config.cooling_system == "cooling_pipes":
            # Dual vertical cryo-refrigeration conduits on side edges
            for side in (-1.0, 1.0):
                px = side * ((rack_w / 2.0) - 0.04)
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.03,
                    depth=rack_h * 0.9,
                    segments=5,
                    offset=mathutils.Vector((px, rack_h / 2.0, front_z + 0.02)),
                    axis='Y',
                    mat_idx=m_idx.get("pipe_industrial", 0),
                    rgba=rgba.get("pipe_industrial", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

        # 4. Top Overhead Cable Conduit
        if config.has_cable_conduit:
            conduit_pos = mathutils.Vector((0.0, rack_h + 0.04, 0.0))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.05,
                depth=rack_w * 0.9,
                segments=5,
                offset=conduit_pos,
                axis='X',
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.3, 0.3, 0.3, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 5. Side Louvers
        if config.has_side_louvers:
            for side in (-1.0, 1.0):
                for v in range(3):
                    vy = (rack_h * 0.4) + (v * 0.18)
                    vent_offset = mathutils.Vector((side * (rack_w / 2.0 + 0.004), vy, 0.0))
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((0.01, 0.04, rack_d * 0.5)),
                        offset=vent_offset,
                        mat_idx=m_idx.get("switch_base", 0),
                        rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                        color_layer=col_layer
                    )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
