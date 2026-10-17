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
from .config import CrashCartConfig

class CrashCartGenerator(BaseAssetGenerator[CrashCartConfig]):
    """
    Procedural generator for industrial/medical emergency crash carts.
    Replicates authentic PS1 survival horror props (Below Nominal aesthetic).
    """

    def generate(self, config: CrashCartConfig) -> bpy.types.Object:
        self.clean_context()
        rng = random.Random(config.seed)

        # 1. Setup Material Manager with Wear Level & Seed
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

        # Color preset selection for body
        if config.body_color_preset == "hazard_yellow":
            body_rect = PS1TextureAtlas.get_rect("hazard_stripes")
            body_mat = m_idx.get("hazard_yellow", 0)
            body_rgba = rgba.get("hazard_yellow", (0.85, 0.65, 0.1, 1.0))
        elif config.body_color_preset == "dirty_beige":
            body_rect = PS1TextureAtlas.get_rect("beige_plastic_worn")
            body_mat = m_idx.get("crt_frame", 0)
            body_rgba = rgba.get("crt_frame", (0.7, 0.68, 0.6, 1.0))
        else:
            # Default red emergency
            body_rect = PS1TextureAtlas.get_rect("red_paint_worn")
            body_mat = m_idx.get("casing_red", m_idx.get("door_emergency_red", 0))
            body_rgba = rgba.get("casing_red", (0.6, 0.1, 0.08, 1.0))

        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")
        switch_rect = PS1TextureAtlas.get_rect("switch_metal")
        crt_rect = PS1TextureAtlas.get_rect("crt_screen_green" if config.monitor_phosphor_color == "green" else "crt_screen_amber")

        cart_w = config.width
        cart_h = config.height
        cart_d = config.depth
        caster_h = config.caster_height

        # Coordinate System:
        # X: Width (-cart_w/2 to +cart_w/2)
        # Y: Height (0 at floor, +caster_h at bottom of body, +caster_h + cart_h at top)
        # Z: Depth (front is +Z, back is -Z, center is 0)

        body_base_y = caster_h
        body_center_y = body_base_y + (cart_h / 2.0)
        body_top_y = body_base_y + cart_h

        # -------------------------------------------------------------------------
        # 1. Main Cart Chassis Body
        # -------------------------------------------------------------------------
        # Main body box
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((cart_w, cart_h, cart_d)),
            offset=mathutils.Vector((0.0, body_center_y, 0.0)),
            mat_idx=body_mat,
            rgba=body_rgba,
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=body_rect
        )

        # Top surface tray lip / retaining rim (stops supplies from rolling off)
        rim_h = 0.025
        rim_thick = 0.02
        # Back rim
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((cart_w, rim_h, rim_thick)),
            offset=mathutils.Vector((0.0, body_top_y + rim_h / 2.0, -cart_d / 2.0 + rim_thick / 2.0)),
            mat_idx=m_idx.get("mounting", 0),
            rgba=rgba.get("mounting", (0.3, 0.3, 0.3, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_light_rect
        )
        # Left and Right rims
        for side in (-1.0, 1.0):
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((rim_thick, rim_h, cart_d)),
                offset=mathutils.Vector((side * (cart_w / 2.0 - rim_thick / 2.0), body_top_y + rim_h / 2.0, 0.0)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.3, 0.3, 0.3, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect
            )

        # -------------------------------------------------------------------------
        # 2. Drawers & Slide Extensions
        # -------------------------------------------------------------------------
        num_drawers = max(1, min(6, config.drawer_count))
        drawer_margin_x = 0.04
        drawer_margin_y = 0.04
        usable_drawer_w = cart_w - (drawer_margin_x * 2.0)
        usable_drawer_h = cart_h - (drawer_margin_y * 2.0)
        each_drawer_h = (usable_drawer_h / num_drawers) - 0.015

        front_z = cart_d / 2.0

        for i in range(num_drawers):
            # i = 0 is top drawer, i = num_drawers - 1 is bottom drawer
            # Calculate Y position
            drawer_y = (body_top_y - drawer_margin_y) - (i + 0.5) * (usable_drawer_h / num_drawers)

            # Slide amount calculation
            if config.drawer_open_mode == "all_closed":
                slide = 0.0
            elif config.drawer_open_mode == "top_open":
                slide = config.drawer_slide_max if i == 0 else 0.0
            elif config.drawer_open_mode == "all_open":
                slide = config.drawer_slide_max * (0.6 + 0.4 * rng.random())
            else:
                # "staggered" (as shown in reference screenshot)
                decay = max(0.0, 1.0 - (i * 0.35))
                slide = config.drawer_slide_max * decay

            drawer_center_z = front_z + slide

            # Drawer front face / block
            drawer_front_depth = 0.025
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((usable_drawer_w, each_drawer_h, drawer_front_depth)),
                offset=mathutils.Vector((0.0, drawer_y, drawer_center_z + drawer_front_depth / 2.0)),
                mat_idx=body_mat,
                rgba=body_rgba,
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=body_rect
            )

            # If drawer is slid open, generate the drawer box sides and slide runners!
            if slide > 0.015:
                # Drawer interior cavity (sides and floor)
                side_thick = 0.012
                box_d = slide + 0.02
                box_z = front_z + (slide / 2.0)

                # Floor plate
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((usable_drawer_w - side_thick * 2, side_thick, box_d)),
                    offset=mathutils.Vector((0.0, drawer_y - each_drawer_h / 2.0 + side_thick / 2.0, box_z)),
                    mat_idx=m_idx.get("steel_dark", m_idx.get("casing_inner", 0)),
                    rgba=rgba.get("steel_dark", (0.2, 0.2, 0.2, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )

                # Left and right drawer sides (sheet metal)
                for side in (-1.0, 1.0):
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((side_thick, each_drawer_h * 0.85, box_d)),
                        offset=mathutils.Vector((side * (usable_drawer_w / 2.0 - side_thick / 2.0), drawer_y, box_z)),
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.35, 0.35, 0.35, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect
                    )

            # Drawer Handle
            handle_z = drawer_center_z + drawer_front_depth + 0.012
            if config.drawer_handle_style == "metal_bar":
                # Horizontal tubular handle
                handle_len = usable_drawer_w * 0.55
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.009,
                    depth=handle_len,
                    segments=4,
                    offset=mathutils.Vector((0.0, drawer_y, handle_z)),
                    axis='X',
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )
                # Two mounting standoffs
                for post_side in (-1.0, 1.0):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.007,
                        depth=0.018,
                        segments=4,
                        offset=mathutils.Vector((post_side * handle_len * 0.45, drawer_y, handle_z - 0.009)),
                        axis='Z',
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect,
                        smooth=False
                    )
            elif config.drawer_handle_style == "recessed_lip":
                # Recessed metal groove
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((usable_drawer_w * 0.6, 0.02, 0.012)),
                    offset=mathutils.Vector((0.0, drawer_y + each_drawer_h * 0.25, drawer_center_z + drawer_front_depth)),
                    mat_idx=m_idx.get("steel_dark", m_idx.get("casing_inner", 0)),
                    rgba=rgba.get("steel_dark", (0.1, 0.1, 0.1, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_dark_rect
                )

        # -------------------------------------------------------------------------
        # 3. Top Defibrillator / CRT Diagnostic Monitor
        # -------------------------------------------------------------------------
        if config.has_top_monitor:
            mon_w = config.monitor_width
            mon_h = config.monitor_height
            mon_d = config.monitor_depth
            mon_y = body_top_y + (mon_h / 2.0) + rim_h
            mon_z = -cart_d * 0.05  # Slightly set back on top shelf

            # Main monitor housing (beige worn retro casing)
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((mon_w, mon_h, mon_d)),
                offset=mathutils.Vector((0.0, mon_y, mon_z)),
                mat_idx=m_idx.get("crt_frame", 0),
                rgba=rgba.get("crt_frame", (0.72, 0.70, 0.62, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )

            # CRT screen (left side of monitor face)
            screen_w = mon_w * 0.50
            screen_h = mon_h * 0.65
            screen_x = -mon_w * 0.18
            screen_z = mon_z + (mon_d / 2.0) + 0.008

            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((screen_w, screen_h, 0.012)),
                offset=mathutils.Vector((screen_x, mon_y, screen_z)),
                mat_idx=m_idx.get("crt_screen_green", 0),
                rgba=rgba.get("crt_screen_green", (0.15, 0.95, 0.35, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=crt_rect
            )

            # Knobs and control dials on the right side of monitor
            if config.has_monitor_knobs:
                knob_x = mon_w * 0.25
                for ki, ky_off in enumerate((-0.035, 0.035)):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.022,
                        depth=0.02,
                        segments=6,
                        offset=mathutils.Vector((knob_x, mon_y + ky_off, screen_z + 0.008)),
                        axis='Z',
                        mat_idx=m_idx.get("switch_metal", 0),
                        rgba=rgba.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=switch_rect,
                        smooth=False
                    )

            # Top carrying handle for defibrillator
            if config.has_monitor_handle:
                handle_bar_w = mon_w * 0.55
                handle_top_y = mon_y + (mon_h / 2.0) + 0.035
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.008,
                    depth=handle_bar_w,
                    segments=4,
                    offset=mathutils.Vector((0.0, handle_top_y, mon_z)),
                    axis='X',
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )
                for h_side in (-1.0, 1.0):
                    MeshBuilder.add_cylinder(
                        bm=bm,
                        radius=0.007,
                        depth=0.035,
                        segments=4,
                        offset=mathutils.Vector((h_side * (handle_bar_w / 2.0), handle_top_y - 0.0175, mon_z)),
                        axis='Y',
                        mat_idx=m_idx.get("mounting", 0),
                        rgba=rgba.get("mounting", (0.7, 0.7, 0.7, 1.0)),
                        color_layer=col_layer,
                        uv_layer=uv_layer,
                        uv_rect=metal_light_rect,
                        smooth=False
                    )

        # -------------------------------------------------------------------------
        # 4. Side Push Handle (Hospital/Maintenance Trolley Bar)
        # -------------------------------------------------------------------------
        if config.has_push_handle:
            h_side = -1.0 if config.push_handle_side == "left" else 1.0
            handle_x = h_side * ((cart_w / 2.0) + 0.065)
            handle_y = body_top_y - 0.06
            bar_len = cart_d * 0.75

            # Main horizontal grip bar
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.012,
                depth=bar_len,
                segments=4,
                offset=mathutils.Vector((handle_x, handle_y, 0.0)),
                axis='Y',
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.75, 0.75, 0.78, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect,
                smooth=False
            )
            # Two support standoffs connecting to cart side
            for z_off in (-bar_len * 0.4, bar_len * 0.4):
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.009,
                    depth=0.065,
                    segments=4,
                    offset=mathutils.Vector((handle_x - h_side * 0.0325, handle_y, z_off)),
                    axis='X',
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.75, 0.75, 0.78, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # 5. Side Oxygen Canister Rack
        # -------------------------------------------------------------------------
        if config.has_oxygen_rack:
            rack_side = 1.0 if config.push_handle_side == "left" else -1.0
            rack_x = rack_side * ((cart_w / 2.0) + 0.08)
            rack_y = body_base_y + (cart_h * 0.4)

            # Bracket cradle
            cradle_w = 0.15
            cradle_d = 0.15
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.08, 0.015, cradle_d)),
                offset=mathutils.Vector((rack_x - rack_side * 0.02, body_base_y + 0.08, 0.0)),
                mat_idx=m_idx.get("steel_dark", m_idx.get("mounting", 0)),
                rgba=rgba.get("steel_dark", (0.3, 0.3, 0.3, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

            # Oxygen Cylinders
            for ti in range(min(2, config.oxygen_tank_count)):
                tank_z = (ti - 0.5 * (config.oxygen_tank_count - 1)) * 0.12
                tank_rad = 0.05
                tank_h = 0.42
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=tank_rad,
                    depth=tank_h,
                    segments=6,
                    offset=mathutils.Vector((rack_x, body_base_y + 0.08 + tank_h / 2.0, tank_z)),
                    axis='Y',
                    mat_idx=m_idx.get("oxygen_cyan", 0),
                    rgba=rgba.get("oxygen_cyan", (0.05, 0.65, 0.75, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow"),
                    smooth=False
                )
                # Brass valve on top of canister
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.018,
                    depth=0.04,
                    segments=4,
                    offset=mathutils.Vector((rack_x, body_base_y + 0.08 + tank_h + 0.02, tank_z)),
                    axis='Y',
                    mat_idx=m_idx.get("switch_metal", 0),
                    rgba=rgba.get("switch_metal", (0.8, 0.7, 0.2, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=switch_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # 6. Swivel Casters / Wheels
        # -------------------------------------------------------------------------
        wheel_r = config.caster_radius
        wheel_thick = 0.028
        inset_x = cart_w * 0.40
        inset_z = cart_d * 0.38

        for corner_x in (-inset_x, inset_x):
            for corner_z in (-inset_z, inset_z):
                # Swivel fork stem (vertical cylinder connecting cart base to wheel axle)
                stem_h = caster_h - wheel_r
                stem_y = caster_h - (stem_h / 2.0)

                # Randomized caster swivel angle (simulates realistic resting position of casters)
                swivel_ang = rng.uniform(0.0, math.pi * 2.0)

                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.014,
                    depth=stem_h,
                    segments=4,
                    offset=mathutils.Vector((corner_x, stem_y, corner_z)),
                    axis='Y',
                    mat_idx=m_idx.get("mounting", 0),
                    rgba=rgba.get("mounting", (0.4, 0.4, 0.4, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )

                # Wheel rubber tire
                wheel_pos = mathutils.Vector((corner_x, wheel_r, corner_z))
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=wheel_r,
                    depth=wheel_thick,
                    segments=6,
                    offset=wheel_pos,
                    axis='X',
                    mat_idx=m_idx.get("rubber_tire", 0),
                    rgba=rgba.get("rubber_tire", (0.1, 0.1, 0.1, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=rubber_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # Finalize BMesh and Align Orientation (Z-up in Blender)
        # -------------------------------------------------------------------------
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

        self.last_generated_object = obj
        return obj

