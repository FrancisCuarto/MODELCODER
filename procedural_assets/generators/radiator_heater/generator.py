import math
import mathutils
import bmesh
import bpy

from ...core.base_generator import BaseAssetGenerator, ValidationReport
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import RadiatorHeaterConfig

class RadiatorHeaterGenerator(BaseAssetGenerator):
    """Procedural generator for industrial space station thermal radiators and convector heaters."""

    def generate(self, config: RadiatorHeaterConfig) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=f"{config.name}_mesh")
        obj = bpy.data.objects.new(name=config.name, object_data=mesh)
        bpy.context.collection.objects.link(obj)

        mat_mgr = self.get_material_manager(config)
        mat_mgr.assign_to_mesh(obj)

        bm = bmesh.new()
        color_layer = bm.loops.layers.color.new("Col")
        uv_layer = bm.loops.layers.uv.new("UVMap")

        w = config.width
        h = config.height
        d = config.depth
        half_w = w * 0.5
        half_h = h * 0.5
        half_d = d * 0.5

        # Materials
        m_casing = mat_mgr.get_index("wall_bulkhead")
        r_casing = mat_mgr.get_rect("metal_dark_grime")

        m_fin = mat_mgr.get_index("wall_support_beam")
        r_fin = mat_mgr.get_rect("metal_light_brushed")

        m_pipe = mat_mgr.get_index("pipe_industrial")
        r_pipe = mat_mgr.get_rect("metal_light_brushed")

        m_valve = mat_mgr.get_index("valve_red")
        r_valve = mat_mgr.get_rect("red_paint_worn")

        m_glow = mat_mgr.get_index("memory_cartridge")
        r_glow = mat_mgr.get_rect("cartridge_amber")

        m_grill = mat_mgr.get_index("vent")
        r_grill = mat_mgr.get_rect("vent_grill")

        m_rust = mat_mgr.get_index("rust_patch")
        r_rust = mat_mgr.get_rect("rust_heavy")

        m_knob = mat_mgr.get_index("button_gray")
        r_knob = mat_mgr.get_rect("beige_plastic_worn")

        m_led = mat_mgr.get_index("led_red")
        r_led = mat_mgr.get_rect("led_red")

        # -------------------------------------------------------------
        # TYPE 1: WALL RADIATOR WITH EXTRUDED FINS
        # -------------------------------------------------------------
        if config.heater_type == "wall_radiator_fins":
            fin_count = max(4, min(14, config.fin_count))
            fin_thick = 0.025
            fin_gap = (w - (fin_count * fin_thick)) / (fin_count + 1)

            # Top & Bottom horizontal header manifolds
            pipe_rad = 0.028
            for pz in [0.10, h - 0.10]:
                MeshBuilder.add_cylinder(
                    bm,
                    radius=pipe_rad,
                    depth=w,
                    segments=6,
                    offset=mathutils.Vector((0.0, 0.0, pz)),
                    axis='X',
                    mat_idx=m_pipe,
                    uv_layer=uv_layer,
                    uv_rect=r_pipe,
                    color_layer=color_layer
                )

            # Vertical heating fins
            fin_h = h - 0.20
            fin_z = h * 0.5
            for i in range(fin_count):
                fx = -half_w + fin_gap + (fin_thick * 0.5) + (i * (fin_thick + fin_gap))
                # Battered bent fin effect if damage
                fy = 0.0
                if config.damage_state == "battered_bent_fins" and (i == 2 or i == fin_count - 3):
                    fy = 0.035
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((fin_thick, d * 0.75, fin_h)),
                    offset=mathutils.Vector((fx, fy, fin_z)),
                    mat_idx=m_fin,
                    uv_layer=uv_layer,
                    uv_rect=r_fin,
                    color_layer=color_layer,
                    rgba=(0.38, 0.40, 0.42, 1.0)
                )

            # Wall Mounting Brackets (on back +Y)
            bracket_w = 0.035
            for bx in [-half_w * 0.65, half_w * 0.65]:
                for bz in [0.15, h - 0.15]:
                    MeshBuilder.add_box(
                        bm,
                        size=mathutils.Vector((bracket_w, half_d + 0.04, 0.06)),
                        offset=mathutils.Vector((bx, half_d * 0.5 + 0.02, bz)),
                        mat_idx=m_pipe,
                        uv_layer=uv_layer,
                        uv_rect=r_pipe,
                        color_layer=color_layer
                    )

            # Steam / Coolant Supply Pipe & Shutoff Handwheel Valve
            if config.has_steam_pipe:
                # Vertical supply drop on right (+X)
                valve_x = half_w + 0.08
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.022,
                    depth=h * 0.55,
                    segments=6,
                    offset=mathutils.Vector((valve_x, 0.0, h - 0.25)),
                    axis='Z',
                    mat_idx=m_pipe,
                    uv_layer=uv_layer,
                    uv_rect=r_pipe,
                    color_layer=color_layer
                )
                # Red Handwheel
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.065,
                    depth=0.025,
                    segments=8,
                    offset=mathutils.Vector((valve_x, -0.06, h - 0.10)),
                    axis='Y',
                    mat_idx=m_valve,
                    uv_layer=uv_layer,
                    uv_rect=r_valve,
                    color_layer=color_layer,
                    rgba=(0.75, 0.15, 0.12, 1.0)
                )

        # -------------------------------------------------------------
        # TYPE 2: CONVECTOR BLOWER CABINET
        # -------------------------------------------------------------
        elif config.heater_type == "convector_blower":
            # Sheet metal shroud
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((w, d, h)),
                offset=mathutils.Vector((0.0, 0.0, half_h)),
                mat_idx=m_casing,
                uv_layer=uv_layer,
                uv_rect=r_casing,
                color_layer=color_layer,
                rgba=(0.28, 0.30, 0.32, 1.0)
            )
            # Front upper hot air exhaust louvers
            vent_w = w * 0.70
            vent_h = h * 0.32
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((vent_w, 0.015, vent_h)),
                offset=mathutils.Vector((-w * 0.08, -half_d - 0.008, h * 0.65)),
                mat_idx=m_grill,
                uv_layer=uv_layer,
                uv_rect=r_grill,
                color_layer=color_layer
            )
            # Internal glowing heating element behind grill
            if config.is_operational:
                MeshBuilder.add_box(
                    bm,
                    size=mathutils.Vector((vent_w * 0.85, 0.02, 0.04)),
                    offset=mathutils.Vector((-w * 0.08, -half_d + 0.03, h * 0.65)),
                    mat_idx=m_glow,
                    uv_layer=uv_layer,
                    uv_rect=r_glow,
                    color_layer=color_layer,
                    rgba=(0.95, 0.50, 0.10, 1.0)
                )
            # Lower cold air intake
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((vent_w, 0.015, h * 0.18)),
                offset=mathutils.Vector((-w * 0.08, -half_d - 0.008, h * 0.20)),
                mat_idx=m_grill,
                uv_layer=uv_layer,
                uv_rect=r_grill,
                color_layer=color_layer
            )
            # Control panel on upper right
            ctrl_x = half_w - 0.09
            # Dial knob
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=0.025,
                segments=8,
                offset=mathutils.Vector((ctrl_x, -half_d - 0.015, h * 0.75)),
                axis='Y',
                mat_idx=m_knob,
                uv_layer=uv_layer,
                uv_rect=r_knob,
                color_layer=color_layer
            )
            # Pilot LED
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.02, 0.01, 0.02)),
                offset=mathutils.Vector((ctrl_x, -half_d - 0.008, h * 0.60)),
                mat_idx=m_led,
                uv_layer=uv_layer,
                uv_rect=r_led,
                color_layer=color_layer,
                rgba=(0.95, 0.10, 0.10, 1.0)
            )

        # -------------------------------------------------------------
        # TYPE 3: SPACE TOWER HEATER (Free-standing pedestal)
        # -------------------------------------------------------------
        else:
            base_rad = w * 0.45
            # Circular base pedestal
            MeshBuilder.add_cylinder(
                bm,
                radius=base_rad,
                depth=0.06,
                segments=10,
                offset=mathutils.Vector((0.0, 0.0, 0.03)),
                axis='Z',
                mat_idx=m_casing,
                uv_layer=uv_layer,
                uv_rect=r_casing,
                color_layer=color_layer
            )
            # Central cylindrical body
            body_rad = w * 0.32
            MeshBuilder.add_cylinder(
                bm,
                radius=body_rad,
                depth=h - 0.12,
                segments=8,
                offset=mathutils.Vector((0.0, 0.0, half_h + 0.02)),
                axis='Z',
                mat_idx=m_grill,
                uv_layer=uv_layer,
                uv_rect=r_grill,
                color_layer=color_layer
            )
            # Top cap
            MeshBuilder.add_cylinder(
                bm,
                radius=body_rad + 0.02,
                depth=0.06,
                segments=8,
                offset=mathutils.Vector((0.0, 0.0, h - 0.03)),
                axis='Z',
                mat_idx=m_casing,
                uv_layer=uv_layer,
                uv_rect=r_casing,
                color_layer=color_layer
            )
            # Central Glowing Quartz Heating Tube
            if config.is_operational:
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.04,
                    depth=h * 0.65,
                    segments=6,
                    offset=mathutils.Vector((0.0, 0.0, half_h)),
                    axis='Z',
                    mat_idx=m_glow,
                    uv_layer=uv_layer,
                    uv_rect=r_glow,
                    color_layer=color_layer,
                    rgba=(0.98, 0.55, 0.12, 1.0)
                )

        # Damage: Leaking burst pipe
        if config.damage_state == "leaking_burst":
            MeshBuilder.add_box(
                bm,
                size=mathutils.Vector((0.35, 0.25, 0.005)),
                offset=mathutils.Vector((0.15, -half_d - 0.05, 0.003)),
                mat_idx=m_rust,
                uv_layer=uv_layer,
                uv_rect=r_rust,
                color_layer=color_layer,
                rgba=(0.45, 0.18, 0.08, 1.0)
            )

        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        return obj

    def validate(self, obj: bpy.types.Object, config: RadiatorHeaterConfig) -> ValidationReport:
        return super().validate(obj, config)
