import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from .config import LockerConfig

class LockerGenerator(BaseAssetGenerator[LockerConfig]):
    """Procedural generator for crew lockers, benches and cabinets (PSX low-poly)."""

    def generate(self, config: LockerConfig) -> bpy.types.Object:
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

        cols = max(1, min(4, config.columns))
        total_w = cols * config.column_width
        total_h = config.height
        total_d = config.depth

        # 1. Main Outer Enclosure Cabinet
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((total_w, total_h, total_d)),
            offset=mathutils.Vector((0.0, total_h / 2.0, 0.0)),
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
            color_layer=col_layer
        )

        # 2. Bottom Stand / Kickplate
        kickplate_h = 0.10
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((total_w * 0.96, kickplate_h, total_d * 0.95)),
            offset=mathutils.Vector((0.0, kickplate_h / 2.0, 0.0)),
            mat_idx=m_idx.get("mounting", 0),
            rgba=rgba.get("mounting", (0.2, 0.2, 0.2, 1.0)),
            color_layer=col_layer
        )

        # 3. Locker Doors
        door_w = config.column_width * 0.94
        door_h = total_h - kickplate_h - 0.04
        door_d = 0.02
        start_x = -(total_w / 2.0) + (config.column_width / 2.0)
        front_z = (total_d / 2.0) + 0.015

        for c in range(cols):
            cx = start_x + (c * config.column_width)
            cy = kickplate_h + (door_h / 2.0) + 0.01

            is_open = (config.door_state == "one_open" and c == 0)

            if is_open:
                # Open door rotated ~65 degrees outward
                angle = math.radians(65)
                hinge_x = cx - (door_w / 2.0)
                door_center_x = hinge_x + math.cos(angle) * (door_w / 2.0)
                door_center_z = front_z + math.sin(angle) * (door_w / 2.0)

                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((door_w * 0.85, door_h, door_d)),
                    offset=mathutils.Vector((door_center_x, cy, door_center_z)),
                    mat_idx=m_idx.get("locker_gray", 0),
                    rgba=rgba.get("locker_gray", (0.3, 0.32, 0.34, 1.0)),
                    color_layer=col_layer
                )

                # Interior shelf visible
                shelf_y = cy + (door_h * 0.25)
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((door_w * 0.95, 0.02, total_d * 0.85)),
                    offset=mathutils.Vector((cx, shelf_y, 0.0)),
                    mat_idx=m_idx.get("casing_inner", 0),
                    rgba=rgba.get("casing_inner", (0.25, 0.25, 0.25, 1.0)),
                    color_layer=col_layer
                )

            else:
                # Closed door panel
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((door_w, door_h, door_d)),
                    offset=mathutils.Vector((cx, cy, front_z)),
                    mat_idx=m_idx.get("locker_gray", 0),
                    rgba=rgba.get("locker_gray", (0.3, 0.32, 0.34, 1.0)),
                    color_layer=col_layer
                )

                # Ventilation Louvers
                if config.has_louvers:
                    for louver_group_y in (cy + (door_h * 0.35), cy - (door_h * 0.35)):
                        for s in range(3):
                            sy = louver_group_y + (s * 0.025)
                            MeshBuilder.add_box(
                                bm=bm,
                                size=mathutils.Vector((door_w * 0.55, 0.008, 0.012)),
                                offset=mathutils.Vector((cx, sy, front_z + 0.01)),
                                mat_idx=m_idx.get("switch_base", 0),
                                rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                                color_layer=col_layer
                            )

                # Handle / Latch
                handle_y = cy
                handle_x = cx + (door_w * 0.32)
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.025, 0.12, 0.02)),
                    offset=mathutils.Vector((handle_x, handle_y, front_z + 0.015)),
                    mat_idx=m_idx.get("switch_metal", 0),
                    rgba=rgba.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
                    color_layer=col_layer
                )

                # Number Plaque
                if config.has_number_plates:
                    plate_y = cy + (door_h * 0.22)
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((door_w * 0.35, 0.05, 0.008)),
                        offset=mathutils.Vector((cx, plate_y, front_z + 0.012)),
                        mat_idx=m_idx.get("screw", 0),
                        rgba=rgba.get("screw", (0.5, 0.5, 0.5, 1.0)),
                        color_layer=col_layer
                    )

        # 4. Integrated Station Bench in Front
        if config.has_integrated_bench:
            bench_h = 0.45
            bench_d = 0.35
            bench_z = (total_d / 2.0) + (bench_d / 2.0) + 0.05
            # Bench seat plank
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((total_w, 0.04, bench_d)),
                offset=mathutils.Vector((0.0, bench_h, bench_z)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.35, 0.32, 0.28, 1.0)),
                color_layer=col_layer
            )
            # Bench leg supports
            for bx in (-total_w * 0.4, total_w * 0.4):
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.04, bench_h, bench_d * 0.8)),
                    offset=mathutils.Vector((bx, bench_h / 2.0, bench_z)),
                    mat_idx=m_idx.get("casing", 0),
                    rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                    color_layer=col_layer
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

