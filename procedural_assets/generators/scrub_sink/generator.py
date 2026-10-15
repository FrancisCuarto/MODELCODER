import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import ScrubSinkConfig

class ScrubSinkGenerator(BaseGenerator):
    """Generates stainless steel surgical scrub sinks with gooseneck faucets and foot pedals."""

    def generate(self, config: ScrubSinkConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_casing = mat_mgr.get_material_index("casing")
        m_stain = mat_mgr.get_material_index("rust_patch")
        m_drain = mat_mgr.get_material_index("rubber_tire")
        m_soap = mat_mgr.get_material_index("chemical_barrel_blue")

        basin_h = 0.35
        rim_z = 0.85
        backsplash_h = h - rim_z

        # 1. Backsplash Wall Panel
        back_th = 0.03
        back_y = -(d / 2) + back_th / 2
        MeshBuilder.add_box(bm, (0, back_y, (rim_z + h) / 2), (w, back_th, backsplash_h), m_steel, "backsplash_panel")

        # Polished non-reflective stainless steel mirror plate
        if config.has_splash_mirror:
            mir_w = w * 0.65
            mir_h = backsplash_h * 0.60
            MeshBuilder.add_box(bm, (0, back_y + 0.015, rim_z + backsplash_h * 0.55), (mir_w, 0.01, mir_h), m_steel, "mirror_plate")

        # Antiseptic soap dispenser
        if config.has_soap_dispenser:
            soap_x = (w / 2) - 0.12
            soap_z = rim_z + 0.18
            MeshBuilder.add_box(bm, (soap_x, back_y + 0.04, soap_z), (0.09, 0.08, 0.16), m_steel, "soap_housing")
            # Clear blue reservoir window
            MeshBuilder.add_box(bm, (soap_x, back_y + 0.08, soap_z - 0.02), (0.06, 0.02, 0.08), m_soap, "soap_window")
            # Push bar
            MeshBuilder.add_box(bm, (soap_x, back_y + 0.08, soap_z - 0.09), (0.07, 0.04, 0.02), m_steel, "soap_pump_lever")

        # 2. Deep Surgical Wash Basin
        basin_z = rim_z - basin_h / 2
        basin_y = 0.02
        basin_w = w
        basin_d = d - back_th

        # Outer apron shroud
        MeshBuilder.add_box(bm, (0, basin_y, basin_z), (basin_w, basin_d, basin_h), m_steel, "basin_apron")
        # Dark inner basin depression
        MeshBuilder.add_box(bm, (0, basin_y, rim_z - 0.02), (basin_w - 0.06, basin_d - 0.06, 0.02), m_casing, "basin_inner")

        # Central drain grate
        drain_z = rim_z - 0.01
        MeshBuilder.add_cylinder(bm, (0, basin_y, drain_z), 0.045, 0.01, sides=8, mat_idx=m_drain, name="drain_grate")

        # Blood / Chemical drain stain
        if config.drain_state == "blood_stained":
            MeshBuilder.add_box(bm, (0.02, basin_y - 0.02, drain_z + 0.005), (0.16, 0.14, 0.002), m_stain, "drain_blood_stain")

        # 3. High Gooseneck Faucet
        faucet_base_z = rim_z + 0.02
        faucet_y = back_y + 0.06
        # Vertical riser
        MeshBuilder.add_cylinder(bm, (0, faucet_y, faucet_base_z + 0.10), 0.015, 0.20, sides=6, mat_idx=m_steel, name="faucet_stem")
        # Curved gooseneck arch
        f_mid = Vector((0, faucet_y + 0.05, faucet_base_z + 0.26))
        f_spout = Vector((0, faucet_y + 0.14, faucet_base_z + 0.18))
        MeshBuilder.add_extruded_cable(bm, [Vector((0, faucet_y, faucet_base_z + 0.20)), f_mid, f_spout], radius=0.014, sides=4, mat_idx=m_steel, name="faucet_gooseneck")

        # 4. Long Elbow-Blade Surgical Operating Levers
        if config.faucet_type == "elbow_blade_levers":
            for lx in (-0.08, 0.08):
                # Lever mount
                MeshBuilder.add_cylinder(bm, (lx, faucet_y, faucet_base_z + 0.03), 0.018, 0.04, sides=6, mat_idx=m_steel, name="lever_hub")
                # Long flat blade extending forward
                MeshBuilder.add_box(bm, (lx, faucet_y + 0.08, faucet_base_z + 0.04), (0.015, 0.16, 0.025), m_steel, "elbow_blade")

        # 5. Lower Pedestal Shroud / Wall Drain Pipe
        p_pipe_start = Vector((0, basin_y, rim_z - basin_h))
        p_pipe_end = Vector((0, back_y, 0.35))
        MeshBuilder.add_extruded_cable(bm, [p_pipe_start, p_pipe_end], radius=0.025, sides=6, mat_idx=m_steel, name="p_trap_drain")

        # Foot pedal valves on floor
        if config.faucet_type == "foot_pedal_valves":
            for px in (-0.07, 0.07):
                MeshBuilder.add_box(bm, (px, basin_y + 0.10, 0.04), (0.05, 0.14, 0.03), m_steel, "foot_pedal")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
