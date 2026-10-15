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
from .config import TerminalConfig

class TerminalGenerator(BaseAssetGenerator[TerminalConfig]):
    """Procedural generator for diegetic computer terminals with rich retrofuturistic variants."""

    def generate(self, config: TerminalConfig) -> bpy.types.Object:
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

        chassis_w = config.width
        chassis_h = config.height
        chassis_d = config.depth

        # 1. Main Enclosure & Mounting Base
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((chassis_w, chassis_h, chassis_d)),
            offset=mathutils.Vector((0.0, 0.0, chassis_d / 2.0)),
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
            color_layer=col_layer
        )

        if config.terminal_type == "pedestal":
            # Pedestal support column underneath
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.065,
                depth=0.85,
                segments=6,
                offset=mathutils.Vector((0.0, -(chassis_h / 2.0) - 0.425, chassis_d * 0.4)),
                axis='Y',
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.25, 0.25, 0.25, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            # Floor circular base plate
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.25,
                depth=0.03,
                segments=6,
                offset=mathutils.Vector((0.0, -(chassis_h / 2.0) - 0.85, chassis_d * 0.4)),
                axis='Y',
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
        elif config.terminal_type == "desktop":
            # Rubber feet under console
            for fx in (-chassis_w * 0.4, chassis_w * 0.4):
                for fz in (chassis_d * 0.2, chassis_d * 0.8):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.025,
                        depth=0.018,
                        segments=4,
                        offset=mathutils.Vector((fx, -(chassis_h / 2.0) - 0.009, fz)),
                        axis='Y',
                        mat_idx=m_idx.get("switch_base", 0),
                        rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                        color_layer=col_layer,
                        smooth=False
                    )

        # 2. CRT Screen with State Variation
        crt_center = mathutils.Vector((0.0, chassis_h * 0.14, chassis_d + 0.02))

        if config.state == "powered_off":
            screen_mat = "crt_frame"
        elif config.state == "alarm":
            screen_mat = "led_red"
        elif config.state == "damaged":
            screen_mat = "crt_frame" if rng.random() > 0.5 else "crt_screen_green"
        else:
            screen_mat = "crt_screen_green" if config.phosphor_color == "green" else "crt_screen_amber"

        MeshBuilder.add_crt_screen(
            bm=bm,
            width=config.screen_w,
            height=config.screen_h,
            bulge=config.crt_bulge,
            offset=crt_center,
            screen_mat_idx=m_idx.get(screen_mat, 0),
            screen_rgba=rgba.get(screen_mat, (0.1, 0.9, 0.3, 1.0)),
            frame_mat_idx=m_idx.get("crt_frame", 0),
            frame_rgba=rgba.get("crt_frame", (0.1, 0.1, 0.1, 1.0)),
            color_layer=col_layer
        )

        # 3. Keycard Reader Slot (Left or Right)
        if config.has_card_reader:
            slot_side = -1.0 if config.card_reader_side == "left" else 1.0
            card_slot_x = slot_side * ((config.screen_w / 2.0) + 0.05)
            card_slot_y = crt_center.y - 0.02
            card_pos = mathutils.Vector((card_slot_x, card_slot_y, chassis_d + 0.025))

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.035, 0.09, 0.02)),
                offset=card_pos,
                mat_idx=m_idx.get("hazard_yellow", 0),
                rgba=rgba.get("hazard_yellow", (0.8, 0.6, 0.1, 1.0)),
                color_layer=col_layer
            )
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.012, 0.065, 0.025)),
                offset=mathutils.Vector((card_slot_x, card_slot_y, chassis_d + 0.03)),
                mat_idx=m_idx.get("switch_base", 0),
                rgba=rgba.get("switch_base", (0.05, 0.05, 0.05, 1.0)),
                color_layer=col_layer
            )

        # 4. Floppy / Tape Data Drive Slot
        if config.has_floppy_drive:
            drive_side = 1.0 if config.card_reader_side == "left" else -1.0
            drive_x = drive_side * ((config.screen_w / 2.0) + 0.05)
            drive_y = crt_center.y + 0.05
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.045, 0.022, 0.02)),
                offset=mathutils.Vector((drive_x, drive_y, chassis_d + 0.025)),
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer
            )
            # Eject button
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.012, 0.010, 0.025)),
                offset=mathutils.Vector((drive_x + (drive_side * 0.025), drive_y, chassis_d + 0.026)),
                mat_idx=m_idx.get("button_gray", 0),
                rgba=rgba.get("button_gray", (0.5, 0.5, 0.5, 1.0)),
                color_layer=col_layer
            )

        # 5. Speaker Grill
        if config.has_speaker_grill:
            spk_side = 1.0 if config.card_reader_side == "left" else -1.0
            spk_x = spk_side * ((config.screen_w / 2.0) + 0.05)
            for i in range(3):
                spk_y = crt_center.y - 0.05 - (i * 0.022)
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.04, 0.008, 0.015)),
                    offset=mathutils.Vector((spk_x, spk_y, chassis_d + 0.022)),
                    mat_idx=m_idx.get("switch_base", 0),
                    rgba=rgba.get("switch_base", (0.05, 0.05, 0.05, 1.0)),
                    color_layer=col_layer
                )

        # 6. Keyboard Styles
        if config.keyboard_style in ("integrated", "tray_projecting"):
            kb_w = config.screen_w * 1.15
            kb_h = chassis_h * 0.26
            kb_d = 0.04 if config.keyboard_style == "integrated" else 0.08
            kb_y = -(chassis_h / 2.0) + (kb_h / 2.0) + 0.04
            kb_offset = mathutils.Vector((0.0, kb_y, chassis_d + (kb_d / 2.0)))

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((kb_w, kb_h, kb_d)),
                offset=kb_offset,
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.25, 0.25, 0.25, 1.0)),
                color_layer=col_layer
            )

            # Key block rows
            key_rows = 3
            dy = (kb_h * 0.65) / key_rows
            for r in range(key_rows):
                ky = kb_y - (kb_h * 0.22) + (r * dy)
                key_strip_pos = mathutils.Vector((0.0, ky, chassis_d + kb_d + 0.008))
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((kb_w * 0.85, dy * 0.65, 0.012)),
                    offset=key_strip_pos,
                    mat_idx=m_idx.get("button_gray", 0),
                    rgba=rgba.get("button_gray", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer
                )
        elif config.keyboard_style == "keypad_numeric":
            pad_w = 0.12
            pad_h = 0.15
            pad_y = -(chassis_h / 2.0) + 0.12
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((pad_w, pad_h, 0.03)),
                offset=mathutils.Vector((0.0, pad_y, chassis_d + 0.015)),
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.25, 0.25, 0.25, 1.0)),
                color_layer=col_layer
            )
            # Numeric keys
            for r in range(3):
                for c in range(3):
                    kx = -0.03 + (c * 0.03)
                    ky = pad_y - 0.03 + (r * 0.03)
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((0.02, 0.02, 0.015)),
                        offset=mathutils.Vector((kx, ky, chassis_d + 0.035)),
                        mat_idx=m_idx.get("button_gray", 0),
                        rgba=rgba.get("button_gray", (0.4, 0.4, 0.4, 1.0)),
                        color_layer=col_layer
                    )

        # 7. Status LEDs & Alarms
        led_mat = "led_red" if config.state == "alarm" else ("led_green" if config.state == "active" else "switch_base")
        for i in range(2):
            led_pos = mathutils.Vector((
                (config.screen_w / 2.0) - 0.02 + (i * 0.03),
                crt_center.y + (config.screen_h / 2.0) + 0.03,
                chassis_d + 0.02
            ))
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.01,
                depth=0.012,
                segments=4,
                offset=led_pos,
                axis='Z',
                mat_idx=m_idx.get(led_mat, 0),
                rgba=rgba.get(led_mat, (0.2, 0.9, 0.2, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 8. Hanging Cables
        if config.has_hanging_cables:
            count = max(1, config.cable_count)
            for i in range(count):
                cx = -0.06 + (i * 0.12)
                cable_start = mathutils.Vector((cx, -(chassis_h / 2.0), chassis_d * 0.5))
                drift = rng.uniform(-0.06, 0.06)
                cable_end = mathutils.Vector((cx + drift, -(chassis_h / 2.0) - 0.35, -0.05))
                pts = generate_catenary_cable_points(cable_start, cable_end, segments=4, sag=0.08)
                c_mat = "cable_black" if i == 0 else "cable_hazard"
                MeshBuilder.add_extruded_cable(
                    bm=bm,
                    points=pts,
                    radius=0.011,
                    sides=3,
                    mat_idx=m_idx.get(c_mat, 0),
                    rgba=rgba.get(c_mat, (0.1, 0.1, 0.1, 1.0)),
                    color_layer=col_layer
                )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
