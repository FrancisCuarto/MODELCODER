import math
import mathutils
import bmesh
import bpy
import random
from typing import Optional, List

from ...core.base_generator import BaseAssetGenerator
from ...core.materials import MaterialManager
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from ...core.transform_utils import generate_catenary_cable_points
from .config import CableBundleConfig

class CableBundleGenerator(BaseAssetGenerator[CableBundleConfig]):
    """
    Procedural generator for industrial cable bundles, overhead umbilical lines, and ladder trays.
    """

    def generate(self, config: CableBundleConfig) -> bpy.types.Object:
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

        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")
        hazard_rect = PS1TextureAtlas.get_rect("hazard_stripes")
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        red_paint_rect = PS1TextureAtlas.get_rect("red_paint_worn")

        L = config.length
        half_l = L / 2.0

        # -------------------------------------------------------------------------
        # 1. Terminal Wall Breakout Junction Boxes
        # -------------------------------------------------------------------------
        if config.has_junction_box:
            for j_side in (-1.0, 1.0):
                box_pos = mathutils.Vector((j_side * (half_l + 0.06), 0.0, 0.0))
                # Junction box chassis
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.12, 0.16, 0.12)),
                    offset=box_pos,
                    mat_idx=m_idx.get("casing", 0),
                    rgba=rgba.get("casing", (0.18, 0.19, 0.21, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )
                # Conduit collar
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.045,
                    depth=0.035,
                    segments=4,
                    offset=mathutils.Vector((j_side * (half_l + 0.01), 0.0, 0.0)),
                    axis='X',
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.5, 0.5, 0.5, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # 2. Ladder Rack Tray (if selected)
        # -------------------------------------------------------------------------
        if config.bundle_type == "ladder_rack_tray":
            tray_w = 0.22
            rail_t = 0.02
            # Dual longitudinal siderails
            for r_side in (-tray_w / 2.0, tray_w / 2.0):
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((L, rail_t, rail_t)),
                    offset=mathutils.Vector((0.0, -0.02, r_side)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.35, 0.35, 0.38, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

            # Cross rungs (every 30 cm)
            num_rungs = max(3, int(L / 0.30))
            for ri in range(num_rungs + 1):
                rx = -half_l + ri * (L / num_rungs)
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((rail_t, rail_t * 0.8, tray_w)),
                    offset=mathutils.Vector((rx, -0.02, 0.0)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.35, 0.35, 0.38, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

        # -------------------------------------------------------------------------
        # 3. Individual Sagging / Catenary Cables
        # -------------------------------------------------------------------------
        n_cables = max(2, min(6, config.cable_count))
        cable_mats = [
            ("cable_black", rubber_rect, (0.1, 0.1, 0.1, 1.0)),
            ("cable_hazard", hazard_rect, (0.85, 0.65, 0.1, 1.0)),
            ("cable_red", red_paint_rect, (0.7, 0.1, 0.1, 1.0)),
            ("oxygen_cyan", PS1TextureAtlas.get_rect("oxygen_cyan_glow"), (0.1, 0.7, 0.8, 1.0)),
        ]

        # Resolution budget
        curve_segs = 5 if config.target_tri_budget > 300 else 4
        cable_sides = 3

        for ci in range(n_cables):
            mat_key, c_rect, c_col = cable_mats[ci % len(cable_mats)]
            # Cluster offset
            offset_y = rng.uniform(-0.025, 0.025)
            offset_z = rng.uniform(-0.035, 0.035)

            p_start = mathutils.Vector((-half_l, offset_y, offset_z))
            p_end = mathutils.Vector((half_l, offset_y * 0.8, offset_z * 0.8))

            cable_radius = rng.uniform(0.012, 0.022)
            individual_sag = config.max_sag * rng.uniform(0.75, 1.25)
            if config.bundle_type == "ladder_rack_tray":
                individual_sag = 0.02  # minimal sag on tray

            # Check if this cable is severed
            if config.has_severed_wire and ci == 1:
                # Cable cuts in half and dangles down to floor
                pts = [
                    p_start,
                    mathutils.Vector((-half_l * 0.5, -individual_sag * 0.6, offset_z)),
                    mathutils.Vector((0.0, -individual_sag * 1.5 - 0.25, offset_z + 0.04)),
                    mathutils.Vector((0.05, -individual_sag * 1.5 - 0.45, offset_z + 0.08))
                ]
            else:
                pts = generate_catenary_cable_points(
                    start=p_start,
                    end=p_end,
                    sag=individual_sag,
                    segments=curve_segs
                )

            MeshBuilder.add_extruded_cable(
                bm=bm,
                points=pts,
                radius=cable_radius,
                sides=cable_sides,
                mat_idx=m_idx.get(mat_key, 0),
                rgba=c_col,
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=c_rect
            )

        # -------------------------------------------------------------------------
        # 4. Cable Zip-Ties / Clamp Bands
        # -------------------------------------------------------------------------
        if config.has_support_ties and config.bundle_type != "ladder_rack_tray":
            num_ties = 3
            for ti in range(num_ties):
                tx = -half_l * 0.6 + ti * (L * 0.6 / max(1, num_ties - 1))
                norm_x = (tx + half_l) / L
                sag_at_tie = 4.0 * config.max_sag * norm_x * (1.0 - norm_x)

                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.025, 0.08, 0.08)),
                    offset=mathutils.Vector((tx, -sag_at_tie, 0.0)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.6, 0.6, 0.62, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
