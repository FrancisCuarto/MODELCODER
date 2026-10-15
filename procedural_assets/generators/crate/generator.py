import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from .config import CrateConfig

class CrateGenerator(BaseAssetGenerator[CrateConfig]):
    """Procedural generator for cargo crates, batteries and chemical containers (PSX low-poly)."""

    def generate(self, config: CrateConfig) -> bpy.types.Object:
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

        w, h, d = config.width, config.height, config.depth

        if config.crate_type == "chemical_drum":
            # --- CHEMICAL DRUM (BARREL) ---
            barrel_rad = min(w, d) / 2.0
            drum_mat = "chemical_barrel_yellow" if config.has_hazard_marking else "chemical_barrel_blue"

            # Main barrel body
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=barrel_rad,
                depth=h,
                segments=7,
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                axis='Y',
                mat_idx=m_idx.get(drum_mat, 0),
                rgba=rgba.get(drum_mat, (0.8, 0.6, 0.1, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

            # Rolling Ribs (chimes) around body
            for chime_y in (h * 0.3, h * 0.7):
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=barrel_rad * 1.06,
                    depth=0.035,
                    segments=7,
                    offset=mathutils.Vector((0.0, chime_y, 0.0)),
                    axis='Y',
                    mat_idx=m_idx.get("casing", 0),
                    rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

            # Top threaded bung cap
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.04,
                depth=0.025,
                segments=6,
                offset=mathutils.Vector((barrel_rad * 0.45, h + 0.012, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("screw", 0),
                rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer,
                smooth=False
            )

        elif config.crate_type == "battery_cell":
            # --- HIGH-VOLTAGE INDUSTRIAL BATTERY ---
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w, h, d)),
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                mat_idx=m_idx.get("hazard_yellow", 0),
                rgba=rgba.get("hazard_yellow", (0.85, 0.62, 0.08, 1.0)),
                color_layer=col_layer
            )
            # Heavy Black Base Tray
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 1.05, h * 0.2, d * 1.05)),
                offset=mathutils.Vector((0.0, h * 0.1, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.1, 0.1, 0.1, 1.0)),
                color_layer=col_layer
            )
            # Positive and Negative Terminal Studs on top
            for tx, c_mat in ((-w * 0.28, "button_red"), (w * 0.28, "casing")):
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.045,
                    depth=0.07,
                    segments=6,
                    offset=mathutils.Vector((tx, h + 0.035, 0.0)),
                    axis='Y',
                    mat_idx=m_idx.get(c_mat, 0),
                    rgba=rgba.get(c_mat, (0.8, 0.2, 0.2, 1.0)),
                    color_layer=col_layer,
                    smooth=False
                )

        elif config.crate_type == "medical_crate":
            # --- EMERGENCY MEDICAL CRATE ---
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w, h, d)),
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.8, 0.82, 0.85, 1.0)),
                color_layer=col_layer
            )
            # Red Cross Emblem on Top Lid
            cross_y = h + 0.005
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 0.45, 0.01, d * 0.15)),
                offset=mathutils.Vector((0.0, cross_y, 0.0)),
                mat_idx=m_idx.get("button_red", 0),
                rgba=rgba.get("button_red", (0.9, 0.1, 0.1, 1.0)),
                color_layer=col_layer
            )
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 0.15, 0.01, d * 0.45)),
                offset=mathutils.Vector((0.0, cross_y, 0.0)),
                mat_idx=m_idx.get("button_red", 0),
                rgba=rgba.get("button_red", (0.9, 0.1, 0.1, 1.0)),
                color_layer=col_layer
            )

        else:
            # --- STANDARD CARGO CHEST ---
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w, h, d)),
                offset=mathutils.Vector((0.0, h / 2.0, 0.0)),
                mat_idx=m_idx.get("casing_inner", 0),
                rgba=rgba.get("casing_inner", (0.3, 0.3, 0.3, 1.0)),
                color_layer=col_layer
            )

            # Lid Rim
            lid_h = h * 0.18
            lid_angle = math.radians(20) if config.lid_state == "ajar_open" else 0.0
            lid_y = h - (lid_h / 2.0) + (math.sin(lid_angle) * (w * 0.2))

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 1.04, lid_h, d * 1.04)),
                offset=mathutils.Vector((0.0, lid_y, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.15, 0.15, 1.0)),
                color_layer=col_layer
            )

            # Stacking Corner Bumpers
            if config.has_reinforced_corners:
                b_size = min(w, h, d) * 0.15
                for sx in (-1.0, 1.0):
                    for sy in (0.0, 1.0):
                        for sz in (-1.0, 1.0):
                            cx = sx * ((w / 2.0) - (b_size / 2.0))
                            cy = (b_size / 2.0) if sy == 0.0 else (h - (b_size / 2.0))
                            cz = sz * ((d / 2.0) - (b_size / 2.0))
                            MeshBuilder.add_box(
                                bm=bm,
                                size=mathutils.Vector((b_size * 1.05, b_size * 1.05, b_size * 1.05)),
                                offset=mathutils.Vector((cx, cy, cz)),
                                mat_idx=m_idx.get("mounting", 0),
                                rgba=rgba.get("mounting", (0.2, 0.2, 0.2, 1.0)),
                                color_layer=col_layer
                            )

            # Side Handles
            if config.has_handles:
                for side in (-1.0, 1.0):
                    hx = side * ((w / 2.0) + 0.02)
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((0.04, 0.05, d * 0.35)),
                        offset=mathutils.Vector((hx, h * 0.6, 0.0)),
                        mat_idx=m_idx.get("screw", 0),
                        rgba=rgba.get("screw", (0.4, 0.4, 0.4, 1.0)),
                        color_layer=col_layer
                    )

            # Front Latch Clasps
            if config.has_latches:
                for lx in (-w * 0.25, w * 0.25):
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((0.04, 0.08, 0.025)),
                        offset=mathutils.Vector((lx, h * 0.78, (d / 2.0) + 0.015)),
                        mat_idx=m_idx.get("switch_metal", 0),
                        rgba=rgba.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
                        color_layer=col_layer
                    )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
