import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import HydroponicTrayBedConfig

class HydroponicTrayBedGenerator(BaseGenerator):
    """Generates space station hydroponic growth beds with nutrient basins, foliage, and UV lamps."""

    def generate(self, config: HydroponicTrayBedConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_frame = mat_mgr.get_material_index("casing")
        m_tray = mat_mgr.get_material_index("locker_gray")
        m_pipe = mat_mgr.get_material_index("pipe_industrial")
        m_valve = mat_mgr.get_material_index("valve_red")

        # Color for plants & lights
        if config.plant_state == "healthy_green":
            m_plant = mat_mgr.get_material_index("led_green")
        elif config.plant_state == "withered_dead":
            m_plant = mat_mgr.get_material_index("rust_patch")
        else: # mutated_spores
            m_plant = mat_mgr.get_material_index("crt_screen_amber")

        # UV grow light material
        if config.uv_light_state == "on_violet":
            m_uv = mat_mgr.get_material_index("sign_sector") # deep blue/violet glow
        elif config.uv_light_state == "flickering":
            m_uv = mat_mgr.get_material_index("sign_exit")
        else:
            m_uv = mat_mgr.get_material_index("casing_inner")

        # 1. Base Support Stanchions
        table_z = 0.60
        leg_th = 0.05
        x_leg = (w / 2) - 0.08
        y_leg = (d / 2) - 0.08

        for lx in (-x_leg, x_leg):
            for ly in (-y_leg, y_leg):
                MeshBuilder.add_box(bm, (lx, ly, table_z / 2), (leg_th, leg_th, table_z), m_frame, "leg")

        # Horizontal stretcher rails
        MeshBuilder.add_box(bm, (0, -y_leg, 0.15), (w - 0.16, 0.04, 0.04), m_frame, "rail_front")
        MeshBuilder.add_box(bm, (0, y_leg, 0.15), (w - 0.16, 0.04, 0.04), m_frame, "rail_rear")

        # 2. Nutrient Solution Recirculating Pipe Manifold
        if config.fluid_pipes:
            # Low pipe along length
            pipe_y = -y_leg - 0.04
            MeshBuilder.add_cylinder(bm, (0, pipe_y, 0.25), 0.022, w - 0.10, sides=6, axis='X', mat_idx=m_pipe, name="feed_pipe")
            # Red flow shutoff valve
            MeshBuilder.add_cylinder(bm, (w * 0.35, pipe_y - 0.03, 0.25), 0.045, 0.02, sides=6, axis='Y', mat_idx=m_valve, name="flow_valve")

        # 3. Main Hydroponics Nutrient Growth Tray
        tray_h = 0.14
        tray_z = table_z + tray_h / 2
        # Outer tray box
        MeshBuilder.add_box(bm, (0, 0, tray_z), (w, d, tray_h), m_tray, "growth_tray_tub")
        # Dark inner nutrient reservoir substrate
        sub_h = 0.06
        sub_z = table_z + sub_h / 2 + 0.02
        MeshBuilder.add_box(bm, (0, 0, sub_z), (w - 0.08, d - 0.08, sub_h), m_frame, "substrate_bed")

        # 4. Low-Poly Vegetation Rows
        plant_rows = 3
        plant_cols = 5
        x_step = (w - 0.24) / max(1, plant_cols - 1)
        y_step = (d - 0.24) / max(1, plant_rows - 1)

        for r in range(plant_rows):
            py = -(d - 0.24) / 2 + r * y_step
            for c in range(plant_cols):
                px = -(w - 0.24) / 2 + c * x_step
                p_h = random.uniform(0.12, 0.20)
                p_r = random.uniform(0.05, 0.08)
                plant_z = table_z + 0.08 + p_h / 2

                if config.plant_state == "healthy_green":
                    # Angular leafy dome / cluster
                    MeshBuilder.add_cylinder(bm, (px, py, plant_z), p_r, p_h, sides=6, mat_idx=m_plant, name="plant_cluster")
                elif config.plant_state == "withered_dead":
                    # Thin dried stalk
                    MeshBuilder.add_box(bm, (px, py, plant_z), (0.02, 0.02, p_h), m_plant, "dead_stalk")
                else: # mutated_spores
                    # Bulbous spore pod
                    MeshBuilder.add_cylinder(bm, (px, py, plant_z), p_r * 1.2, p_h * 0.8, sides=8, mat_idx=m_plant, name="spore_pod")

        # 5. Overhead Arch Frame & UV Grow Light Fixture
        arch_top_z = h
        arch_post_x = (w / 2) - 0.04
        # Left & Right upright arch pillars
        for ax in (-arch_post_x, arch_post_x):
            MeshBuilder.add_box(bm, (ax, 0, (table_z + h) / 2), (0.04, 0.04, h - table_z), m_frame, "uv_arch_post")

        # Top horizontal crossbeam
        MeshBuilder.add_box(bm, (0, 0, arch_top_z - 0.02), (w, 0.04, 0.04), m_frame, "uv_crossbeam")

        # UV Grow Light Luminaire Reflector
        lum_w = w * 0.75
        lum_d = d * 0.40
        lum_z = arch_top_z - 0.08
        MeshBuilder.add_box(bm, (0, 0, lum_z), (lum_w, lum_d, 0.04), m_tray, "uv_reflector_hood")
        # Dual UV glowing emission tubes
        for ty in (-lum_d * 0.25, lum_d * 0.25):
            MeshBuilder.add_cylinder(bm, (0, ty, lum_z - 0.025), 0.018, lum_w - 0.08, sides=6, axis='X', mat_idx=m_uv, name="uv_tube")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
