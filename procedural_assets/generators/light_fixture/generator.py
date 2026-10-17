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
from .config import LightFixtureConfig

class LightFixtureGenerator(BaseAssetGenerator[LightFixtureConfig]):
    """
    Procedural generator for industrial luminaires, ceiling troffers, and bulkhead cage lights.
    """

    def generate(self, config: LightFixtureConfig) -> bpy.types.Object:
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
        uv_layer = bm.loops.layers.uv.new("UVMap")

        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")
        tube_lit_rect = PS1TextureAtlas.get_rect("fluorescent_lit")
        tube_off_rect = PS1TextureAtlas.get_rect("crt_screen_off")
        red_beacon_rect = PS1TextureAtlas.get_rect("door_seal_red")

        L = config.length
        W = config.width
        D = config.depth

        if config.fixture_type == "bulkhead_cage":
            # ---------------------------------------------------------------------
            # Bulkhead Wall Light with Steel Cage
            # ---------------------------------------------------------------------
            # Base plate
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((W, L * 0.45, D * 0.4)),
                offset=mathutils.Vector((0.0, 0.0, -D * 0.2)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.18, 0.19, 0.21, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )
            # Glass prism dome
            lit_mat = m_idx.get("fluorescent_tube_lit", 0) if config.lighting_state != "completely_dead" else m_idx.get("glass_tube", 0)
            lit_rect = tube_lit_rect if config.lighting_state != "completely_dead" else tube_off_rect
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((W * 0.75, L * 0.35, D * 0.6)),
                offset=mathutils.Vector((0.0, 0.0, D * 0.15)),
                mat_idx=lit_mat,
                rgba=(0.9, 0.95, 1.0, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=lit_rect
            )
            # Protective Cage Bars
            if config.has_wire_guard:
                for ci in (-1, 0, 1):
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((W * 0.85, 0.012, 0.012)),
                        offset=mathutils.Vector((0.0, ci * (L * 0.12), D * 0.48)),
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.5, 0.5, 0.5, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect
                    )

        elif config.fixture_type == "emergency_beacon":
            # ---------------------------------------------------------------------
            # Revolving Warning Siren Beacon
            # ---------------------------------------------------------------------
            beacon_rad = W * 0.42
            base_h = 0.04
            dome_h = D * 1.3
            # Base ring
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=beacon_rad,
                depth=base_h,
                segments=8,
                offset=mathutils.Vector((0.0, base_h / 2.0, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.2, 0.2, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect,
                smooth=False
            )
            # Red glowing dome
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=beacon_rad * 0.85,
                depth=dome_h,
                segments=6,
                offset=mathutils.Vector((0.0, base_h + dome_h / 2.0, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("led_red", m_idx.get("door_emergency_red", 0)),
                rgba=(0.95, 0.1, 0.08, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=red_beacon_rect,
                smooth=False
            )

        else:
            # ---------------------------------------------------------------------
            # Fluorescent Troffer Ceiling Fixture (Standard)
            # ---------------------------------------------------------------------
            # Main sheet metal reflector housing
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((W, D, L)),
                offset=mathutils.Vector((0.0, -D / 2.0, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.25, 0.26, 0.28, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

            # End caps with wiring knockouts
            for end_side in (-1.0, 1.0):
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((W * 1.02, D * 1.05, 0.02)),
                    offset=mathutils.Vector((0.0, -D / 2.0, end_side * (L / 2.0 + 0.01))),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

            # Fluorescent Tubes
            num_tubes = max(1, min(3, config.tube_count))
            tube_spacing = W / (num_tubes + 1)
            tube_rad = 0.016
            tube_len = L * 0.94

            for ti in range(num_tubes):
                tx = - (W / 2.0) + (ti + 1) * tube_spacing

                # Determine if this specific tube is illuminated
                is_dead = False
                if config.lighting_state == "completely_dead":
                    is_dead = True
                elif config.lighting_state == "flickering_one_dead" and ti == 1:
                    is_dead = True

                if is_dead:
                    tube_mat = m_idx.get("glass_tube", 0)
                    t_rect = tube_off_rect
                    t_rgba = (0.2, 0.22, 0.24, 1.0)
                else:
                    tube_mat = m_idx.get("fluorescent_tube_lit", 0)
                    t_rect = tube_lit_rect
                    t_rgba = (0.85, 0.95, 0.98, 1.0)

                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=tube_rad,
                    depth=tube_len,
                    segments=4,
                    offset=mathutils.Vector((tx, -D * 0.65, 0.0)),
                    axis='Z',
                    mat_idx=tube_mat,
                    rgba=t_rgba,
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=t_rect,
                    smooth=False
                )

                # Socket sockets on both ends
                for side_z in (-1.0, 1.0):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=tube_rad * 1.3,
                        depth=0.025,
                        segments=4,
                        offset=mathutils.Vector((tx, -D * 0.65, side_z * (tube_len / 2.0))),
                        axis='Z',
                        mat_idx=m_idx.get("switch_base", 0),
                        rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=rubber_rect,
                        smooth=False
                    )

            # Steel wire cage grid guard
            if config.has_wire_guard:
                cage_ribs = 5
                for ri in range(cage_ribs):
                    rz = -(L * 0.42) + ri * (L * 0.84 / (cage_ribs - 1))
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((W * 0.95, 0.008, 0.008)),
                        offset=mathutils.Vector((0.0, -D * 0.88, rz)),
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.6, 0.6, 0.6, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect
                    )

        # -------------------------------------------------------------------------
        # Dangling Wire (Loose electrical hazard)
        # -------------------------------------------------------------------------
        if config.has_dangling_wire:
            wire_pts = [
                mathutils.Vector((W * 0.35, -D / 2.0, L * 0.45)),
                mathutils.Vector((W * 0.38, -D * 1.4, L * 0.42)),
                mathutils.Vector((W * 0.32, -D * 2.8, L * 0.44)),
                mathutils.Vector((W * 0.36, -D * 3.6, L * 0.41))
            ]
            MeshBuilder.add_extruded_cable(
                bm=bm,
                points=wire_pts,
                radius=0.008,
                sides=3,
                mat_idx=m_idx.get("cable_black", 0),
                rgba=rgba.get("cable_black", (0.1, 0.1, 0.1, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=rubber_rect
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

