import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from .config import DoorConfig

class DoorGenerator(BaseAssetGenerator[DoorConfig]):
    """Procedural generator for industrial doors, airlocks and emergency bulkheads (PSX low-poly)."""

    def generate(self, config: DoorConfig) -> bpy.types.Object:
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

        frame_w = config.width
        frame_h = config.height
        frame_d = config.frame_depth
        thick = config.frame_thickness

        if config.door_type == "emergency_bulkhead":
            door_mat = "door_emergency_red"
        elif config.door_type == "heavy_airlock":
            door_mat = "casing"
        else:
            door_mat = "door_frame_heavy"

        # 1. Outer Bulkhead Frame (Left jamb, Right jamb, Header)
        left_jamb_x = -(frame_w / 2.0) + (thick / 2.0)
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((thick, frame_h, frame_d)),
            offset=mathutils.Vector((left_jamb_x, frame_h / 2.0, 0.0)),
            mat_idx=m_idx.get("door_frame_heavy", 0),
            rgba=rgba.get("door_frame_heavy", (0.2, 0.2, 0.2, 1.0)),
            color_layer=col_layer
        )
        right_jamb_x = (frame_w / 2.0) - (thick / 2.0)
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((thick, frame_h, frame_d)),
            offset=mathutils.Vector((right_jamb_x, frame_h / 2.0, 0.0)),
            mat_idx=m_idx.get("door_frame_heavy", 0),
            rgba=rgba.get("door_frame_heavy", (0.2, 0.2, 0.2, 1.0)),
            color_layer=col_layer
        )
        header_y = frame_h - (thick / 2.0)
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((frame_w, thick, frame_d * 1.08)),
            offset=mathutils.Vector((0.0, header_y, 0.0)),
            mat_idx=m_idx.get("door_frame_heavy", 0),
            rgba=rgba.get("door_frame_heavy", (0.2, 0.2, 0.2, 1.0)),
            color_layer=col_layer
        )

        # 2. Dual Sliding Door Leaves (Left and Right)
        inner_w = frame_w - (2.0 * thick)
        inner_h = frame_h - thick
        leaf_w = (inner_w / 2.0) + 0.03
        leaf_h = inner_h
        leaf_d = frame_d * 0.22

        max_slide = (inner_w / 2.0) * 0.95
        slide_x = config.open_ratio * max_slide

        left_leaf_x = -(leaf_w / 2.0) - slide_x
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((leaf_w, leaf_h, leaf_d)),
            offset=mathutils.Vector((left_leaf_x, leaf_h / 2.0, 0.0)),
            mat_idx=m_idx.get(door_mat, 0),
            rgba=rgba.get(door_mat, (0.3, 0.3, 0.3, 1.0)),
            color_layer=col_layer
        )
        right_leaf_x = (leaf_w / 2.0) + slide_x
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((leaf_w, leaf_h, leaf_d)),
            offset=mathutils.Vector((right_leaf_x, leaf_h / 2.0, 0.0)),
            mat_idx=m_idx.get(door_mat, 0),
            rgba=rgba.get(door_mat, (0.3, 0.3, 0.3, 1.0)),
            color_layer=col_layer
        )

        # Reinforcing ribs across door leaves
        for rib_y in (leaf_h * 0.25, leaf_h * 0.50, leaf_h * 0.75):
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((leaf_w * 0.88, 0.05, leaf_d + 0.02)),
                offset=mathutils.Vector((left_leaf_x, rib_y, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
                color_layer=col_layer
            )
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((leaf_w * 0.88, 0.05, leaf_d + 0.02)),
                offset=mathutils.Vector((right_leaf_x, rib_y, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
                color_layer=col_layer
            )

        # 3. Reinforced Viewport Window (Allows seeing Europa / adjacent room)
        if config.has_reinforced_window:
            win_y = leaf_h * 0.62
            win_w = leaf_w * 0.38
            win_h = 0.25
            for lx in (left_leaf_x, right_leaf_x):
                # Window Frame
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((win_w, win_h, leaf_d + 0.03)),
                    offset=mathutils.Vector((lx, win_y, 0.0)),
                    mat_idx=m_idx.get("switch_base", 0),
                    rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                    color_layer=col_layer
                )
                # Glass insert
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((win_w * 0.8, win_h * 0.75, leaf_d + 0.035)),
                    offset=mathutils.Vector((lx, win_y, 0.0)),
                    mat_idx=m_idx.get("glass_tube", 0),
                    rgba=rgba.get("glass_tube", (0.2, 0.4, 0.5, 1.0)),
                    color_layer=col_layer
                )

        # 4. Hydraulic / Pneumatic Actuator Pistons Above Door
        if config.has_hydraulic_pistons:
            piston_y = header_y + (thick * 0.15)
            for side in (-1.0, 1.0):
                px = side * (inner_w * 0.35)
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.035,
                    depth=inner_w * 0.45,
                    segments=5,
                    offset=mathutils.Vector((px, piston_y, frame_d * 0.4)),
                    axis='X',
                    mat_idx=m_idx.get("switch_metal", 0),
                    rgba=rgba.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

        # 5. Top Hazard Chevrons / Header Trim
        if config.has_hazard_stripes:
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((inner_w * 0.95, 0.06, (frame_d * 1.08) + 0.01)),
                offset=mathutils.Vector((0.0, header_y - (thick * 0.35), 0.0)),
                mat_idx=m_idx.get("hazard_yellow", 0),
                rgba=rgba.get("hazard_yellow", (0.85, 0.62, 0.08, 1.0)),
                color_layer=col_layer
            )

        # 6. Status Light Bar
        if config.has_status_light:
            if config.open_ratio > 0.4:
                light_color = "led_green"
            elif config.door_type == "emergency_bulkhead":
                light_color = "door_emergency_red"
            else:
                light_color = "led_yellow"

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.22, 0.045, (frame_d * 1.08) + 0.02)),
                offset=mathutils.Vector((0.0, header_y + 0.02, 0.0)),
                mat_idx=m_idx.get(light_color, 0),
                rgba=rgba.get(light_color, (0.2, 0.9, 0.2, 1.0)),
                color_layer=col_layer
            )

        # 7. Access Control Interface
        if config.access_interface == "card_reader":
            reader_pos = mathutils.Vector((right_jamb_x, frame_h * 0.48, (frame_d / 2.0) + 0.02))
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((thick * 0.65, 0.18, 0.04)),
                offset=reader_pos,
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.3, 0.3, 0.3, 1.0)),
                color_layer=col_layer
            )
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.012,
                depth=0.015,
                segments=4,
                offset=mathutils.Vector((reader_pos.x, reader_pos.y + 0.05, reader_pos.z + 0.02)),
                axis='Z',
                mat_idx=m_idx.get("led_green", 0),
                rgba=rgba.get("led_green", (0.1, 0.9, 0.2, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
        elif config.access_interface == "manual_wheel":
            # Big wheel on left leaf
            wheel_pos = mathutils.Vector((left_leaf_x, leaf_h * 0.5, leaf_d + 0.04))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.18,
                depth=0.03,
                segments=6,
                offset=wheel_pos,
                axis='Z',
                mat_idx=m_idx.get("valve_red", 0),
                rgba=rgba.get("valve_red", (0.8, 0.1, 0.1, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
