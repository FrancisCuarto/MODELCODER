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
from .config import OfficeDeskConfig

class OfficeDeskGenerator(BaseAssetGenerator[OfficeDeskConfig]):
    """
    Procedural generator for industrial laboratory and office desks.
    Fits the brutalist retrofuturistic PS1 survival horror aesthetic of Below Nominal.
    """

    def generate(self, config: OfficeDeskConfig) -> bpy.types.Object:
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

        # Texture Rectangles
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")

        if config.surface_material == "beige_formica":
            top_rect = PS1TextureAtlas.get_rect("beige_plastic_worn")
            top_mat = m_idx.get("crt_frame", 0)
            top_rgba = rgba.get("crt_frame", (0.7, 0.68, 0.6, 1.0))
        elif config.surface_material == "hazard":
            top_rect = PS1TextureAtlas.get_rect("hazard_stripes")
            top_mat = m_idx.get("hazard_yellow", 0)
            top_rgba = rgba.get("hazard_yellow", (0.85, 0.65, 0.1, 1.0))
        else:
            top_rect = metal_dark_rect
            top_mat = m_idx.get("casing", 0)
            top_rgba = rgba.get("casing", (0.2, 0.22, 0.24, 1.0))

        w = config.width
        h = config.height
        d = config.depth
        thick = config.desktop_thickness
        top_y = h - (thick / 2.0)

        # -------------------------------------------------------------------------
        # 1. Desktop Work Surface Plate
        # -------------------------------------------------------------------------
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((w, thick, d)),
            offset=mathutils.Vector((0.0, top_y, 0.0)),
            mat_idx=top_mat,
            rgba=top_rgba,
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=top_rect
        )

        # Cable grommet pass-through hole (front-right corner)
        if config.has_cable_grommet:
            grommet_pos = mathutils.Vector((w * 0.38, h + 0.002, -d * 0.35))
            MeshBuilder.add_circle(
                bm=bm,
                radius=0.035,
                segments=6,
                offset=grommet_pos,
                axis='Y',
                mat_idx=m_idx.get("switch_base", 0),
                rgba=rgba.get("switch_base", (0.05, 0.05, 0.05, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=rubber_rect,
                smooth=False
            )

        # -------------------------------------------------------------------------
        # 2. Leg Frame & Support Structure
        # -------------------------------------------------------------------------
        leg_h = h - thick
        leg_t = config.leg_thickness
        inset_x = (w / 2.0) - (leg_t / 2.0) - 0.03
        inset_z = (d / 2.0) - (leg_t / 2.0) - 0.03

        if config.leg_style == "panel_sides":
            # Solid sheet metal end panels
            for side in (-1.0, 1.0):
                panel_x = side * ((w / 2.0) - 0.03)
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.03, leg_h, d * 0.9)),
                    offset=mathutils.Vector((panel_x, leg_h / 2.0, 0.0)),
                    mat_idx=m_idx.get("casing", 0),
                    rgba=rgba.get("casing", (0.18, 0.19, 0.21, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )
        elif config.leg_style == "cantilever_t_frame":
            # Heavy industrial inverted T-base
            for side in (-1.0, 1.0):
                px = side * ((w / 2.0) - 0.08)
                # Upright column
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.06, leg_h, 0.08)),
                    offset=mathutils.Vector((px, leg_h / 2.0, 0.0)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.25, 0.25, 0.28, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )
                # Horizontal foot bar on floor
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((0.06, 0.035, d * 0.85)),
                    offset=mathutils.Vector((px, 0.0175, 0.0)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.25, 0.25, 0.28, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )
        else:
            # "tubular_four_legs"
            for lx in (-inset_x, inset_x):
                for lz in (-inset_z, inset_z):
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((leg_t, leg_h, leg_t)),
                        offset=mathutils.Vector((lx, leg_h / 2.0, lz)),
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.3, 0.3, 0.32, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect
                    )
                    # Rubber foot pad
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((leg_t * 1.15, 0.015, leg_t * 1.15)),
                        offset=mathutils.Vector((lx, 0.0075, lz)),
                        mat_idx=m_idx.get("switch_base", 0),
                        rgba=rgba.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=rubber_rect
                    )

        # -------------------------------------------------------------------------
        # 3. Rear Modesty Panel / Cable Raceway
        # -------------------------------------------------------------------------
        if config.has_rear_cable_raceway:
            modesty_h = leg_h * 0.55
            modesty_y = (h - thick) - (modesty_h / 2.0)
            modesty_z = -inset_z + 0.01
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w - 0.12, modesty_h, 0.018)),
                offset=mathutils.Vector((0.0, modesty_y, modesty_z)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.16, 0.18, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

        # -------------------------------------------------------------------------
        # 4. Storage Pedestals & Sliding Drawers
        # -------------------------------------------------------------------------
        pedestal_sides = []
        if config.pedestal_layout == "left_only":
            pedestal_sides = [-1.0]
        elif config.pedestal_layout == "right_only":
            pedestal_sides = [1.0]
        elif config.pedestal_layout == "dual_pedestals":
            pedestal_sides = [-1.0, 1.0]

        ped_w = min(0.42, w * 0.32)
        ped_h = leg_h * 0.88
        ped_d = d * 0.82
        ped_base_y = leg_h - ped_h

        for p_side in pedestal_sides:
            ped_x = p_side * ((w / 2.0) - (ped_w / 2.0) - 0.05)
            # Pedestal carcass box
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((ped_w, ped_h, ped_d)),
                offset=mathutils.Vector((ped_x, ped_base_y + ped_h / 2.0, 0.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.16, 0.18, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

            # Drawers within pedestal
            n_drawers = max(1, min(4, config.drawer_count_per_pedestal))
            drawer_h = (ped_h - 0.04) / n_drawers
            ped_front_z = ped_d / 2.0

            for di in range(n_drawers):
                dy = (ped_base_y + ped_h - 0.02) - (di + 0.5) * drawer_h

                if config.drawer_open_style == "top_open":
                    d_slide = config.drawer_slide_max if di == 0 else 0.0
                elif config.drawer_open_style == "all_ajar":
                    d_slide = config.drawer_slide_max * max(0.0, 1.0 - di * 0.35)
                else:
                    d_slide = 0.0

                df_z = ped_front_z + d_slide

                # Drawer front slab
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((ped_w - 0.03, drawer_h - 0.012, 0.02)),
                    offset=mathutils.Vector((ped_x, dy, df_z + 0.01)),
                    mat_idx=m_idx.get("casing_inner", 0),
                    rgba=rgba.get("casing_inner", (0.28, 0.29, 0.31, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )

                # Metal bar pull handle
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((ped_w * 0.5, 0.014, 0.015)),
                    offset=mathutils.Vector((ped_x, dy, df_z + 0.025)),
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.7, 0.7, 0.72, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )

        # -------------------------------------------------------------------------
        # 5. Partition Screen / Privacy Divider (Optional)
        # -------------------------------------------------------------------------
        if config.has_partition_screen:
            screen_h = config.partition_height
            screen_y = h + (screen_h / 2.0)
            screen_z = -(d / 2.0) + 0.02
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w * 0.96, screen_h, 0.018)),
                offset=mathutils.Vector((0.0, screen_y, screen_z)),
                mat_idx=m_idx.get("crt_frame", 0),
                rgba=rgba.get("crt_frame", (0.55, 0.58, 0.60, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )

        # -------------------------------------------------------------------------
        # 6. Under-Desk CPU / Tower Shelf (Optional)
        # -------------------------------------------------------------------------
        if config.has_under_shelf and config.pedestal_layout != "dual_pedestals":
            shelf_side = -1.0 if config.pedestal_layout == "right_only" else 1.0
            shelf_x = shelf_side * ((w / 2.0) - (ped_w / 2.0) - 0.05)
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((ped_w, 0.02, d * 0.75)),
                offset=mathutils.Vector((shelf_x, 0.12, 0.0)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.3, 0.3, 0.32, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect
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

