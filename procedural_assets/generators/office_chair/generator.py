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
from .config import OfficeChairConfig

class OfficeChairGenerator(BaseAssetGenerator[OfficeChairConfig]):
    """
    Procedural generator for industrial task chairs and flight command seating.
    Authentic PS1 retro aesthetic with vinyl wear, casters, and damaged variants.
    """

    def generate(self, config: OfficeChairConfig) -> bpy.types.Object:
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

        # Atlas UV mappings
        vinyl_rect = PS1TextureAtlas.get_rect("chair_vinyl_dark")
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")

        vinyl_mat = m_idx.get("chair_vinyl", m_idx.get("switch_base", 0))
        vinyl_rgba = rgba.get("chair_vinyl", (0.16, 0.18, 0.20, 1.0))

        if config.upholstery_color == "emergency_red":
            vinyl_rect = PS1TextureAtlas.get_rect("red_paint_worn")
            vinyl_mat = m_idx.get("casing_red", m_idx.get("door_emergency_red", 0))
            vinyl_rgba = rgba.get("casing_red", (0.6, 0.1, 0.08, 1.0))
        elif config.upholstery_color == "industrial_blue":
            vinyl_rect = PS1TextureAtlas.get_rect("sign_sector_blue")
            vinyl_mat = m_idx.get("button_blue", 0)
            vinyl_rgba = rgba.get("button_blue", (0.1, 0.3, 0.5, 1.0))

        sw = config.seat_width
        sd = config.seat_depth
        sh = config.seat_height
        c_thick = config.cushion_thickness

        # -------------------------------------------------------------------------
        # 1. Seat Cushion & Under-Seat Tilt Mechanism
        # -------------------------------------------------------------------------
        seat_y = sh - (c_thick / 2.0)
        # Main seat cushion box
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((sw, c_thick, sd)),
            offset=mathutils.Vector((0.0, seat_y, 0.0)),
            mat_idx=vinyl_mat,
            rgba=vinyl_rgba,
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=vinyl_rect
        )

        # Under-seat steel chassis tray
        mech_h = 0.045
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((sw * 0.75, mech_h, sd * 0.75)),
            offset=mathutils.Vector((0.0, seat_y - (c_thick / 2.0) - (mech_h / 2.0), 0.0)),
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.15, 0.15, 0.17, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_dark_rect
        )

        # Height adjustment lever (sticking out to the right side)
        lever_y = seat_y - (c_thick / 2.0) - (mech_h / 2.0)
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=0.007,
            depth=0.18,
            segments=4,
            offset=mathutils.Vector((sw * 0.38 + 0.05, lever_y, 0.0)),
            axis='X',
            mat_idx=m_idx.get("mounting", 0),
            rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_light_rect,
            smooth=False
        )

        # -------------------------------------------------------------------------
        # 2. Central Pneumatic Column & Base
        # -------------------------------------------------------------------------
        col_top = seat_y - (c_thick / 2.0) - mech_h
        col_bottom = 0.08
        col_len = max(0.1, col_top - col_bottom)

        # Chrome hydraulic gas lift cylinder
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=0.025,
            depth=col_len,
            segments=6,
            offset=mathutils.Vector((0.0, col_bottom + col_len / 2.0, 0.0)),
            axis='Y',
            mat_idx=m_idx.get("mounting", 0),
            rgba=rgba.get("mounting", (0.8, 0.8, 0.82, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_light_rect,
            smooth=False
        )

        if config.base_style == "pedestal_bolted":
            # Round marine bulkhead flange bolted to floor
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=config.base_radius * 0.7,
                depth=0.035,
                segments=6,
                offset=mathutils.Vector((0.0, 0.0175, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.22, 0.24, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect,
                smooth=False
            )
        elif config.base_style == "four_leg_tubular":
            # 4 fixed splayed tubular legs
            leg_rad = config.base_radius * 0.8
            for lang in (math.pi * 0.25, math.pi * 0.75, math.pi * 1.25, math.pi * 1.75):
                fx = math.cos(lang) * leg_rad
                fz = math.sin(lang) * leg_rad
                # Leg strut from center to floor pad
                leg_pts = [mathutils.Vector((0.0, col_bottom, 0.0)), mathutils.Vector((fx, 0.015, fz))]
                MeshBuilder.add_extruded_cable(
                    bm=bm,
                    points=leg_pts,
                    radius=0.016,
                    sides=4,
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect
                )
        else:
            # "five_star_casters" (Standard retro office chair base)
            spokes = max(3, min(6, config.spoke_count))
            hub_rad = 0.045
            b_rad = config.base_radius

            # Central spoke hub
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=hub_rad,
                depth=0.05,
                segments=spokes,
                offset=mathutils.Vector((0.0, col_bottom, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.15, 0.15, 0.17, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect,
                smooth=False
            )

            # Radial spoke arms and caster wheels
            for s in range(spokes):
                ang = (2.0 * math.pi * s) / spokes
                cos_a = math.cos(ang)
                sin_a = math.sin(ang)

                tip_x = cos_a * b_rad
                tip_z = sin_a * b_rad
                mid_x = tip_x * 0.5
                mid_z = tip_z * 0.5

                # Arm beam
                arm_len = b_rad - hub_rad
                arm_rot = mathutils.Matrix.Rotation(-ang, 4, 'Y')
                arm_size = mathutils.Vector((0.035, 0.025, arm_len))
                arm_center = mathutils.Vector((mid_x, col_bottom - 0.015, mid_z))

                MeshBuilder.add_box(
                    bm=bm,
                    size=arm_size,
                    offset=arm_center,
                    mat_idx=m_idx.get("casing", 0),
                    rgba=rgba.get("casing", (0.18, 0.19, 0.21, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )

                # Wheel caster at arm tip
                wheel_r = 0.026
                wheel_thick = 0.022
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=wheel_r,
                    depth=wheel_thick,
                    segments=4,
                    offset=mathutils.Vector((tip_x, wheel_r, tip_z)),
                    axis='X',
                    mat_idx=m_idx.get("rubber_tire", 0),
                    rgba=rgba.get("rubber_tire", (0.1, 0.1, 0.1, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=rubber_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # 3. Backrest & Structural Spine
        # -------------------------------------------------------------------------
        tilt_rad = math.radians(config.backrest_tilt)
        back_h = config.backrest_height
        back_w = sw * 0.86
        back_d = c_thick * 0.85

        # Steel spine bracket from under-seat up to backrest
        spine_start = mathutils.Vector((0.0, seat_y - 0.02, -sd * 0.35))
        spine_corner = mathutils.Vector((0.0, seat_y + 0.05, -sd * 0.52))
        spine_top = mathutils.Vector((0.0, seat_y + back_h * 0.6, -sd * 0.52 - math.sin(tilt_rad) * back_h * 0.5))

        MeshBuilder.add_extruded_cable(
            bm=bm,
            points=[spine_start, spine_corner, spine_top],
            radius=0.018,
            sides=4,
            mat_idx=m_idx.get("casing", 0),
            rgba=rgba.get("casing", (0.2, 0.2, 0.22, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_dark_rect
        )

        # Backrest cushion
        back_center_y = seat_y + (back_h / 2.0) + 0.06
        back_center_z = -sd * 0.48 - math.sin(tilt_rad) * (back_h / 2.0)

        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((back_w, back_h, back_d)),
            offset=mathutils.Vector((0.0, back_center_y, back_center_z)),
            mat_idx=vinyl_mat,
            rgba=vinyl_rgba,
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=vinyl_rect
        )

        # Upper headrest (if high back style)
        if config.backrest_style == "high_back_headrest":
            head_h = 0.18
            head_w = back_w * 0.70
            head_y = back_center_y + (back_h / 2.0) + (head_h / 2.0) + 0.02
            head_z = back_center_z - math.sin(tilt_rad) * (head_h / 2.0)
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((head_w, head_h, back_d * 0.9)),
                offset=mathutils.Vector((0.0, head_y, head_z)),
                mat_idx=vinyl_mat,
                rgba=vinyl_rgba,
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=vinyl_rect
            )

        # -------------------------------------------------------------------------
        # 4. Armrests (Both, One Broken, or None)
        # -------------------------------------------------------------------------
        if config.armrest_style in ("both", "one_broken"):
            arm_h = config.armrest_height
            arm_len = sd * 0.65
            pad_w = 0.055
            pad_t = 0.025

            for side in (-1.0, 1.0):
                is_broken = (side == 1.0 and config.armrest_style == "one_broken")
                ax = side * ((sw / 2.0) + 0.04)

                if is_broken:
                    # Broken armrest: jagged snapped upright post, no arm pad!
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.014,
                        depth=arm_h * 0.45,
                        segments=4,
                        offset=mathutils.Vector((ax, seat_y + arm_h * 0.22, 0.0)),
                        axis='Y',
                        mat_idx=m_idx.get("casing", 0),
                        rgba=rgba.get("casing", (0.25, 0.25, 0.28, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_dark_rect,
                        smooth=False
                    )
                else:
                    # Full intact armrest
                    # Upright support post
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.014,
                        depth=arm_h,
                        segments=4,
                        offset=mathutils.Vector((ax, seat_y + arm_h / 2.0, 0.0)),
                        axis='Y',
                        mat_idx=m_idx.get("casing", 0),
                        rgba=rgba.get("casing", (0.25, 0.25, 0.28, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_dark_rect,
                        smooth=False
                    )
                    # Padded top rest
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((pad_w, pad_t, arm_len)),
                        offset=mathutils.Vector((ax, seat_y + arm_h + pad_t / 2.0, 0.0)),
                        mat_idx=vinyl_mat,
                        rgba=vinyl_rgba,
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=vinyl_rect
                    )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
