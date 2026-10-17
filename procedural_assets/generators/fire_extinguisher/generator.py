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
from .config import FireExtinguisherConfig

class FireExtinguisherGenerator(BaseAssetGenerator[FireExtinguisherConfig]):
    """
    Procedural generator for wall-mounted extinguishers and emergency stations.
    """

    def generate(self, config: FireExtinguisherConfig) -> bpy.types.Object:
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

        red_paint_rect = PS1TextureAtlas.get_rect("red_paint_worn")
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")
        gauge_rect = PS1TextureAtlas.get_rect("gauge_meter")
        rubber_rect = PS1TextureAtlas.get_rect("rubber_black")
        door_seal_rect = PS1TextureAtlas.get_rect("door_seal_red")

        tank_r = config.tank_radius
        tank_h = config.tank_height

        tank_center_z = tank_r + 0.04  # offset forward from wall
        tank_center_y = 0.0

        # -------------------------------------------------------------------------
        # 1. Cabinet or Wall Bracket
        # -------------------------------------------------------------------------
        if config.mount_style == "emergency_cabinet":
            cab_w = config.cabinet_width
            cab_h = config.cabinet_height
            cab_d = config.cabinet_depth

            # Cabinet outer box
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((cab_w, cab_h, cab_d)),
                offset=mathutils.Vector((0.0, 0.0, cab_d / 2.0)),
                mat_idx=m_idx.get("door_emergency_red", 0),
                rgba=rgba.get("door_emergency_red", (0.7, 0.1, 0.1, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=door_seal_rect
            )

            # Glass window front panel
            if config.cabinet_glass_state == "intact":
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((cab_w * 0.75, cab_h * 0.75, 0.008)),
                    offset=mathutils.Vector((0.0, 0.0, cab_d + 0.004)),
                    mat_idx=m_idx.get("glass_tube", 0),
                    rgba=(0.3, 0.6, 0.7, 0.5),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=PS1TextureAtlas.get_rect("crt_screen_off")
                )
            elif config.cabinet_glass_state == "door_open":
                # Swung open door
                door_w = cab_w * 0.92
                MeshBuilder.add_box(
                    bm=bm,
                    size=mathutils.Vector((door_w * 0.7, cab_h * 0.92, 0.015)),
                    offset=mathutils.Vector((-(cab_w / 2.0) - door_w * 0.35, 0.0, cab_d * 0.8)),
                    mat_idx=m_idx.get("door_emergency_red", 0),
                    rgba=rgba.get("door_emergency_red", (0.7, 0.1, 0.1, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=door_seal_rect
                )

            tank_center_z = cab_d * 0.55

        else:
            # Wall bracket backplate & clamp ring
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.08, tank_h * 0.8, 0.015)),
                offset=mathutils.Vector((0.0, 0.0, 0.0075)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.22, 0.24, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )
            # Collar ring
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((tank_r * 2.2, 0.025, tank_r * 2.2)),
                offset=mathutils.Vector((0.0, tank_h * 0.25, tank_center_z)),
                mat_idx=m_idx.get("mounting", 0),
                rgba=rgba.get("mounting", (0.4, 0.4, 0.4, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_light_rect
            )

        # -------------------------------------------------------------------------
        # 2. Main Red Extinguisher Tank Cylinder
        # -------------------------------------------------------------------------
        segments = 6 if config.target_tri_budget < 300 else 8
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=tank_r,
            depth=tank_h,
            segments=segments,
            offset=mathutils.Vector((0.0, tank_center_y, tank_center_z)),
            axis='Y',
            mat_idx=m_idx.get("casing_red", m_idx.get("door_emergency_red", 0)),
            rgba=(0.75, 0.12, 0.10, 1.0),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=red_paint_rect,
            smooth=False
        )

        # Bottom foot ring
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=tank_r * 1.04,
            depth=0.035,
            segments=segments,
            offset=mathutils.Vector((0.0, -tank_h / 2.0 + 0.0175, tank_center_z)),
            axis='Y',
            mat_idx=m_idx.get("switch_base", 0),
            rgba=(0.1, 0.1, 0.1, 1.0),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=rubber_rect,
            smooth=False
        )

        # -------------------------------------------------------------------------
        # 3. Valve Head Assembly & Squeeze Lever
        # -------------------------------------------------------------------------
        valve_y = tank_h / 2.0 + 0.035
        # Valve neck block
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=tank_r * 0.35,
            depth=0.07,
            segments=6,
            offset=mathutils.Vector((0.0, valve_y, tank_center_z)),
            axis='Y',
            mat_idx=m_idx.get("switch_metal", 0),
            rgba=(0.75, 0.72, 0.65, 1.0),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_light_rect,
            smooth=False
        )

        # Upper squeeze lever
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((0.02, 0.012, 0.12)),
            offset=mathutils.Vector((0.0, valve_y + 0.035, tank_center_z + 0.03)),
            mat_idx=m_idx.get("casing_red", 0),
            rgba=(0.75, 0.1, 0.1, 1.0),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=red_paint_rect
        )

        # Carry handle lever below
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((0.02, 0.012, 0.10)),
            offset=mathutils.Vector((0.0, valve_y + 0.012, tank_center_z + 0.02)),
            mat_idx=m_idx.get("casing_red", 0),
            rgba=(0.75, 0.1, 0.1, 1.0),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=red_paint_rect
        )

        # Pressure gauge dial (facing forward)
        if config.has_pressure_gauge:
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.018,
                depth=0.015,
                segments=6,
                offset=mathutils.Vector((0.0, valve_y, tank_center_z + tank_r * 0.35 + 0.015)),
                axis='Z',
                mat_idx=m_idx.get("gauge", 0),
                rgba=(0.9, 0.9, 0.9, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=gauge_rect,
                smooth=False
            )

        # -------------------------------------------------------------------------
        # 4. Discharge Rubber Hose & Nozzle Horn
        # -------------------------------------------------------------------------
        if config.has_hose_nozzle:
            hose_pts = [
                mathutils.Vector((-tank_r * 0.3, valve_y, tank_center_z)),
                mathutils.Vector((-tank_r * 1.3, valve_y - 0.05, tank_center_z)),
                mathutils.Vector((-tank_r * 1.25, -tank_h * 0.15, tank_center_z + tank_r * 0.6)),
                mathutils.Vector((0.0, -tank_h * 0.25, tank_center_z + tank_r * 1.05))
            ]
            MeshBuilder.add_extruded_cable(
                bm=bm,
                points=hose_pts,
                radius=0.012,
                sides=4,
                mat_idx=m_idx.get("cable_black", 0),
                rgba=(0.1, 0.1, 0.1, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=rubber_rect
            )
            # Horn nozzle at tip
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=0.018,
                depth=0.06,
                segments=4,
                offset=mathutils.Vector((0.0, -tank_h * 0.25, tank_center_z + tank_r * 1.10)),
                axis='Z',
                mat_idx=m_idx.get("switch_base", 0),
                rgba=(0.12, 0.12, 0.12, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=rubber_rect,
                smooth=False
            )

        # -------------------------------------------------------------------------
        # 5. Identification Placard Sign above Extinguisher
        # -------------------------------------------------------------------------
        if config.has_wall_sign and config.mount_style != "emergency_cabinet":
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((0.18, 0.14, 0.008)),
                offset=mathutils.Vector((0.0, tank_h / 2.0 + 0.18, 0.004)),
                mat_idx=m_idx.get("door_emergency_red", 0),
                rgba=(0.8, 0.1, 0.1, 1.0),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=door_seal_rect
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

