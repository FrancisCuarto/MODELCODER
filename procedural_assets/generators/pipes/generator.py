import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from .config import PipeConfig

class PipeGenerator(BaseAssetGenerator[PipeConfig]):
    """Procedural generator for industrial pipes, valves and pressure assemblies (PSX low-poly)."""

    def generate(self, config: PipeConfig) -> bpy.types.Object:
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

        rad = config.radius * (1.3 if config.has_insulation_layer else 1.0)
        pipe_len = config.length
        pipe_mat = "casing_inner" if config.has_insulation_layer else "pipe_industrial"

        # 1. Geometry based on pipe_type
        if config.pipe_type == "elbow_90":
            # Horizontal run (half length)
            h_len = pipe_len * 0.5
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad,
                depth=h_len,
                segments=6,
                offset=mathutils.Vector((h_len / 2.0, 0.0, 0.0)),
                axis='X',
                mat_idx=m_idx.get(pipe_mat, 0),
                rgba=rgba.get(pipe_mat, (0.35, 0.38, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            # Corner junction cube
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((rad * 2.4, rad * 2.4, rad * 2.4)),
                offset=mathutils.Vector((0.0, 0.0, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer
            )
            # Vertical downward run
            v_len = pipe_len * 0.5
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad,
                depth=v_len,
                segments=6,
                offset=mathutils.Vector((0.0, -v_len / 2.0, 0.0)),
                axis='Y',
                mat_idx=m_idx.get(pipe_mat, 0),
                rgba=rgba.get(pipe_mat, (0.35, 0.38, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        elif config.pipe_type == "t_junction":
            # Main horizontal run
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad,
                depth=pipe_len,
                segments=6,
                offset=mathutils.Vector((0.0, 0.0, 0.0)),
                axis='X',
                mat_idx=m_idx.get(pipe_mat, 0),
                rgba=rgba.get(pipe_mat, (0.35, 0.38, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            # Perpendicular Tee branch
            tee_len = pipe_len * 0.38
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad * 0.85,
                depth=tee_len,
                segments=6,
                offset=mathutils.Vector((0.0, tee_len / 2.0, 0.0)),
                axis='Y',
                mat_idx=m_idx.get(pipe_mat, 0),
                rgba=rgba.get(pipe_mat, (0.35, 0.38, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        else:
            # Straight run / valve assembly
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad,
                depth=pipe_len,
                segments=6,
                offset=mathutils.Vector((0.0, 0.0, 0.0)),
                axis='X',
                mat_idx=m_idx.get(pipe_mat, 0),
                rgba=rgba.get(pipe_mat, (0.35, 0.38, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        # 2. Bolted Flange Couplings
        if config.has_flange_couplings:
            for side in (-1.0, 1.0):
                fx = side * ((pipe_len / 2.0) - 0.03)
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=rad * 1.55,
                    depth=0.04,
                    segments=6,
                    offset=mathutils.Vector((fx, 0.0, 0.0)),
                    axis='X',
                    mat_idx=m_idx.get("screw", 0),
                    rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

        # 3. Valve Assembly (Handwheel vs Lever)
        if config.pipe_type == "valve_assembly" or config.valve_type != "none":
            # Central valve body block
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((rad * 2.8, rad * 2.4, rad * 2.4)),
                offset=mathutils.Vector((0.0, 0.0, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer
            )

            spindle_h = rad * 2.6
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=rad * 0.25,
                depth=spindle_h,
                segments=5,
                offset=mathutils.Vector((0.0, (spindle_h / 2.0) + rad, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("switch_metal", 0),
                rgba=rgba.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

            wheel_y = rad + spindle_h

            if config.valve_type == "lever_quarter_turn":
                # Quarter-turn Lever Handle
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((rad * 2.5, 0.02, 0.04)),
                    offset=mathutils.Vector((rad * 1.0, wheel_y, 0.0)),
                    mat_idx=m_idx.get("hazard_yellow", 0),
                    rgba=rgba.get("hazard_yellow", (0.85, 0.62, 0.08, 1.0)),
                    color_layer=col_layer
                )
            else:
                # Spoked Handwheel (Red)
                wheel_rad = rad * 1.85
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=wheel_rad,
                    depth=0.025,
                    segments=6,
                    offset=mathutils.Vector((0.0, wheel_y, 0.0)),
                    axis='Y',
                    mat_idx=m_idx.get("valve_red", 0),
                    rgba=rgba.get("valve_red", (0.8, 0.15, 0.1, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=rad * 0.4,
                    depth=0.04,
                    segments=5,
                    offset=mathutils.Vector((0.0, wheel_y, 0.0)),
                    axis='Y',
                    mat_idx=m_idx.get("screw", 0),
                    rgba=rgba.get("screw", (0.3, 0.3, 0.3, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((wheel_rad * 1.8, 0.02, 0.02)),
                    offset=mathutils.Vector((0.0, wheel_y, 0.0)),
                    mat_idx=m_idx.get("valve_red", 0),
                    rgba=rgba.get("valve_red", (0.8, 0.15, 0.1, 1.0)),
                    color_layer=col_layer
                )
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.02, 0.02, wheel_rad * 1.8)),
                    offset=mathutils.Vector((0.0, wheel_y, 0.0)),
                    mat_idx=m_idx.get("valve_red", 0),
                    rgba=rgba.get("valve_red", (0.8, 0.15, 0.1, 1.0)),
                    color_layer=col_layer
                )

        # 4. Pressure Gauge Dial
        if config.has_pressure_gauge:
            gauge_x = pipe_len * 0.28
            gauge_pos = mathutils.Vector((gauge_x, rad + 0.08, 0.0))

            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.015,
                depth=0.08,
                segments=4,
                offset=mathutils.Vector((gauge_x, rad + 0.04, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("screw", 0),
                rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.07,
                depth=0.03,
                segments=6,
                offset=gauge_pos,
                axis='Z',
                mat_idx=m_idx.get("screw", 0),
                rgba=rgba.get("screw", (0.35, 0.35, 0.35, 1.0)),
                color_layer=col_layer,
                smooth=False
            )
            MeshBuilder.add_circle(
                bm=bm,
                radius=0.058,
                segments=6,
                offset=mathutils.Vector((gauge_x, gauge_pos.y, 0.016)),
                axis='Z',
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.85, 0.85, 0.8, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
