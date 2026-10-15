import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import LockerBenchConfig

class LockerBenchGenerator(BaseGenerator):
    """Generates changing room benches with perforated seats, boot racks, and forgotten crew gear."""

    def generate(self, config: LockerBenchConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        length = config.length
        w = config.width
        h = config.height

        m_steel = mat_mgr.get_material_index("mounting")
        m_frame = mat_mgr.get_material_index("casing")
        m_plank = mat_mgr.get_material_index("locker_gray")
        m_boot = mat_mgr.get_material_index("rubber_tire")
        m_gear = mat_mgr.get_material_index("chair_vinyl")

        # 1. Legs / Base Structure
        leg_y_off = (length / 2) - 0.15
        leg_x_off = (w / 2) - 0.06

        if config.leg_style == "slab_sides":
            # 2 Thick flat end plates
            for ly in (-leg_y_off, leg_y_off):
                MeshBuilder.add_box(bm, (0, ly, (h - 0.04) / 2), (w - 0.04, 0.05, h - 0.04), m_frame, "leg_slab")
        else: # tubular_flanged
            tube_r = 0.022
            leg_h = h - 0.04
            for ly in (-leg_y_off, leg_y_off):
                for lx in (-leg_x_off, leg_x_off):
                    # Tubular leg
                    MeshBuilder.add_cylinder(bm, (lx, ly, leg_h / 2), tube_r, leg_h, sides=6, mat_idx=m_frame, name="leg_tube")
                    # Floor flange plate
                    MeshBuilder.add_cylinder(bm, (lx, ly, 0.015), tube_r + 0.025, 0.03, sides=6, mat_idx=m_steel, name="floor_flange")

            # Under-seat longitudinal stringer rails
            MeshBuilder.add_box(bm, (-leg_x_off, 0, h - 0.04), (0.04, length - 0.10, 0.03), m_frame, "rail_L")
            MeshBuilder.add_box(bm, (leg_x_off, 0, h - 0.04), (0.04, length - 0.10, 0.03), m_frame, "rail_R")

        # 2. Lower Mag-Boot Shelf Rack
        if config.has_shoe_shelf:
            shelf_z = 0.14
            # 3 Longitudinal rods
            for rx in (-w * 0.28, 0.0, w * 0.28):
                MeshBuilder.add_cylinder(bm, (rx, 0, shelf_z), 0.01, length - 0.20, sides=4, axis='Y', mat_idx=m_steel, name="boot_rod")
            # Cross supports at legs
            for ly in (-leg_y_off, leg_y_off):
                MeshBuilder.add_box(bm, (0, ly, shelf_z), (w - 0.10, 0.03, 0.02), m_frame, "shelf_crossbar")

        # 3. Top Seat Planks / Perforated Slabs
        seat_z = h - 0.02
        if config.bench_type == "composite_slats":
            # 3 Longitudinal slat planks
            slat_w = (w - 0.06) / 3
            for si in range(3):
                sx = -w / 2 + 0.03 + si * (slat_w + 0.01) + slat_w / 2
                MeshBuilder.add_box(bm, (sx, 0, seat_z), (slat_w, length, 0.035), m_plank, f"slat_{si}")
        else: # perforated_metal or boot_rack_integrated
            # Solid seat with beveled edges
            MeshBuilder.add_box(bm, (0, 0, seat_z), (w, length, 0.04), m_plank, "seat_plank")
            # Steel edge reinforcement brackets
            MeshBuilder.add_box(bm, (0, -length / 2 + 0.02, seat_z), (w + 0.01, 0.04, 0.045), m_steel, "edge_cap_1")
            MeshBuilder.add_box(bm, (0, length / 2 - 0.02, seat_z), (w + 0.01, 0.04, 0.045), m_steel, "edge_cap_2")

        # 4. Forgotten Crew Gear (Abandoned boots or rolled emergency towel)
        if config.has_forgotten_gear:
            # Pair of magnetic boots under bench on shelf
            boot_y = -length * 0.25
            for bx in (-0.08, 0.08):
                MeshBuilder.add_box(bm, (bx, boot_y, 0.22), (0.10, 0.22, 0.12), m_boot, "mag_boot")
            # Rolled survival towel / jacket on seat
            gear_y = length * 0.30
            MeshBuilder.add_cylinder(bm, (0, gear_y, h + 0.06), 0.065, 0.28, sides=8, axis='Y', mat_idx=m_gear, name="rolled_jacket")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
