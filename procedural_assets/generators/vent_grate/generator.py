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
from .config import VentGrateConfig

class VentGrateGenerator(BaseAssetGenerator[VentGrateConfig]):
    """
    Procedural generator for wall/floor HVAC grilles and ventilation shafts.
    """

    def generate(self, config: VentGrateConfig) -> bpy.types.Object:
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

        vent_rect = PS1TextureAtlas.get_rect("vent_grill")
        metal_dark_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        metal_light_rect = PS1TextureAtlas.get_rect("metal_light_brushed")

        w = config.width
        h = config.height
        fd = config.frame_depth
        dd = config.duct_depth

        # -------------------------------------------------------------------------
        # 1. Dark Recessed Duct Cavity Box (Behind wall, extending -Z)
        # -------------------------------------------------------------------------
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((w * 0.88, h * 0.88, dd)),
            offset=mathutils.Vector((0.0, 0.0, -dd / 2.0)),
            mat_idx=m_idx.get("switch_base", 0),
            rgba=rgba.get("switch_base", (0.05, 0.05, 0.06, 1.0)),
            color_layer=col_layer,
            uv_layer=uv_layer,
            uv_rect=metal_dark_rect
        )

        # -------------------------------------------------------------------------
        # 2. Interior Circulation Fan (Inside duct cavity)
        # -------------------------------------------------------------------------
        if config.has_fan_blades:
            fan_z = -dd * 0.65
            hub_rad = min(w, h) * 0.10
            hub_h = 0.035

            # Fan center motor hub
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=hub_rad,
                depth=hub_h,
                segments=6,
                offset=mathutils.Vector((0.0, 0.0, fan_z)),
                axis='Z',
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.2, 0.22, 0.24, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect,
                smooth=False
            )

            # Fan blades radiating outward
            n_blades = max(3, min(6, config.fan_blade_count))
            blade_len = (min(w, h) * 0.38) - hub_rad
            blade_w = hub_rad * 0.95
            blade_t = 0.008
            base_rot = math.radians(config.fan_rotation_deg)

            for bi in range(n_blades):
                ang = base_rot + (2.0 * math.pi * bi) / n_blades
                mid_dist = hub_rad + (blade_len / 2.0)
                bx = math.cos(ang) * mid_dist
                by = math.sin(ang) * mid_dist

                # Blade oriented along radial angle
                blade_geom = bmesh.ops.create_cube(bm, size=1.0)
                b_verts = [v for v in blade_geom["verts"] if isinstance(v, bmesh.types.BMVert)]

                # Scale blade
                rot_blade = mathutils.Matrix.Rotation(ang + math.pi / 2.0, 4, 'Z')
                # Add slight pitch angle to blade
                rot_pitch = mathutils.Matrix.Rotation(math.radians(25.0), 4, 'Y')

                for v in b_verts:
                    v.co.x *= blade_w
                    v.co.y *= blade_len
                    v.co.z *= blade_t
                    v.co = rot_pitch @ v.co
                    v.co = rot_blade @ v.co
                    v.co.x += bx
                    v.co.y += by
                    v.co.z += fan_z

                bm.faces.ensure_lookup_table()
                for f in bm.faces:
                    if all(v in b_verts for v in f.verts):
                        MeshBuilder.apply_face_attributes(f, m_idx.get("mounting", 0), (0.5, 0.5, 0.52, 1.0), col_layer, smooth=False)
                        if uv_layer:
                            MeshBuilder.apply_face_uv_rect(f, uv_layer, metal_light_rect)

        # -------------------------------------------------------------------------
        # 3. Outer Mounting Flange Frame
        # -------------------------------------------------------------------------
        border_w = 0.04
        # Left and Right frame borders
        for side in (-1.0, 1.0):
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((border_w, h, fd)),
                offset=mathutils.Vector((side * ((w / 2.0) - (border_w / 2.0)), 0.0, fd / 2.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.25, 0.26, 0.28, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )
        # Top and Bottom frame borders
        for side in (-1.0, 1.0):
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((w - border_w * 2, border_w, fd)),
                offset=mathutils.Vector((0.0, side * ((h / 2.0) - (border_w / 2.0)), fd / 2.0)),
                mat_idx=m_idx.get("casing", 0),
                rgba=rgba.get("casing", (0.25, 0.26, 0.28, 1.0)),
                color_layer=col_layer,
                uv_layer=uv_layer,
                uv_rect=metal_dark_rect
            )

        # Corner hex bolts
        for sx in (-1.0, 1.0):
            for sy in (-1.0, 1.0):
                # If hanging by one screw, 3 screws are missing!
                if config.grate_state == "hanging_by_one_screw" and not (sx == -1.0 and sy == 1.0):
                    continue
                MeshBuilder.add_cylinder(
                    bm=bm,
                    radius=0.008,
                    depth=0.012,
                    segments=4,
                    offset=mathutils.Vector((sx * (w / 2.0 - border_w / 2.0), sy * (h / 2.0 - border_w / 2.0), fd + 0.006)),
                    axis='Z',
                    mat_idx=m_idx.get("screw", 0),
                    rgba=rgba.get("screw", (0.7, 0.7, 0.7, 1.0)),
                    color_layer=col_layer,
                    uv_layer=uv_layer,
                    uv_rect=metal_light_rect,
                    smooth=False
                )

        # -------------------------------------------------------------------------
        # 4. Front Slotted Louver Grille (Bolted, Hanging, or Removed)
        # -------------------------------------------------------------------------
        if config.grate_state != "removed_open_duct":
            grate_w = w - border_w * 1.5
            grate_h = h - border_w * 1.5
            grate_t = 0.012

            grate_geom = bmesh.ops.create_cube(bm, size=1.0)
            g_verts = [v for v in grate_geom["verts"] if isinstance(v, bmesh.types.BMVert)]

            for v in g_verts:
                v.co.x *= grate_w
                v.co.y *= grate_h
                v.co.z *= grate_t

            if config.grate_state == "hanging_by_one_screw":
                # Rotate around top-left pivot screw
                pivot_x = -(w / 2.0) + (border_w / 2.0)
                pivot_y = (h / 2.0) - (border_w / 2.0)
                hang_rot = mathutils.Matrix.Rotation(-math.radians(config.hanging_angle), 4, 'Z')

                for v in g_verts:
                    # Move to pivot relative, rotate, move back
                    v.co.x -= pivot_x
                    v.co.y -= pivot_y
                    v.co = hang_rot @ v.co
                    v.co.x += pivot_x
                    v.co.y += pivot_y
                    v.co.z += fd * 0.95
            else:
                for v in g_verts:
                    v.co.z += fd * 0.95

            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                if all(v in g_verts for v in f.verts):
                    MeshBuilder.apply_face_attributes(f, m_idx.get("vent", 0), (0.28, 0.30, 0.32, 1.0), col_layer, smooth=False)
                    if uv_layer:
                        MeshBuilder.apply_face_uv_rect(f, uv_layer, vent_rect)

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj
