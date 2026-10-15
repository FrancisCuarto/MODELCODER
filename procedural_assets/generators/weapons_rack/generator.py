import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import WeaponsRackConfig

class WeaponsRackGenerator(BaseGenerator):
    """Generates space station armory security racks with locking bars and firearm silhouettes."""

    def generate(self, config: WeaponsRackConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        d = config.depth
        h = config.height

        m_frame = mat_mgr.get_material_index("casing")
        m_steel = mat_mgr.get_material_index("mounting")
        m_gun = mat_mgr.get_material_index("switch_metal")
        m_lock = mat_mgr.get_material_index("casing_red")
        m_stock = mat_mgr.get_material_index("rubber_tire")

        # 1. Welded A-frame / Upright Steel Frame
        frame_th = 0.045
        for fx in (-w / 2 + frame_th / 2, w / 2 - frame_th / 2):
            # Upright side channel
            MeshBuilder.add_box(bm, (fx, 0, h / 2), (frame_th, d * 0.70, h), m_frame, "side_upright")
            # Base floor skid
            MeshBuilder.add_box(bm, (fx, 0, 0.025), (frame_th + 0.03, d, 0.05), m_steel, "base_skid")

        # Top cap crossbar
        MeshBuilder.add_box(bm, (0, 0, h - 0.03), (w, 0.06, 0.05), m_frame, "top_crossbar")

        # 2. Lower Buttstock Cradle Shelf
        cradle_z = 0.28
        MeshBuilder.add_box(bm, (0, 0, cradle_z), (w - 0.08, d * 0.65, 0.06), m_frame, "buttstock_cradle")
        # Front lip of cradle
        MeshBuilder.add_box(bm, (0, d * 0.28, cradle_z + 0.04), (w - 0.08, 0.03, 0.06), m_steel, "cradle_lip")

        # Lower Ammunition Lockbox
        if config.has_bottom_ammo_box:
            MeshBuilder.add_box(bm, (0, 0, 0.12), (w - 0.12, d * 0.60, 0.18), m_steel, "ammo_chest")
            # Padlock on ammo box
            MeshBuilder.add_cylinder(bm, (0, d * 0.31, 0.12), 0.02, 0.015, sides=6, axis='Y', mat_idx=m_lock, name="ammo_lock")

        # 3. Upper Barrel Rest / Separator Notches
        barrel_z = h * 0.72
        MeshBuilder.add_box(bm, (0, -0.04, barrel_z), (w - 0.08, 0.08, 0.04), m_frame, "barrel_rest_beam")

        # Slots & Weapon Silhouettes
        slots = config.slot_count
        slot_w = (w - 0.16) / max(1, slots)

        for s_idx in range(slots):
            sx = -(w - 0.16) / 2 + (s_idx + 0.5) * slot_w

            # Rubber separator notch tooth
            MeshBuilder.add_box(bm, (sx, -0.04, barrel_z + 0.03), (0.018, 0.08, 0.03), m_stock, f"notch_{s_idx}")

            # Weapon presence based on occupancy
            if random.random() < config.occupancy_ratio:
                # Low-poly riot shotgun / assault rifle silhouette
                gun_len = 0.95
                gun_z = cradle_z + 0.03 + gun_len / 2

                # Receiver & barrel
                MeshBuilder.add_box(bm, (sx, 0.02, gun_z), (0.035, 0.06, gun_len), m_gun, f"weapon_barrel_{s_idx}")
                # Buttstock (thickened bottom)
                MeshBuilder.add_box(bm, (sx, 0.03, cradle_z + 0.15), (0.04, 0.09, 0.24), m_stock, f"weapon_stock_{s_idx}")
                # Pump / forestock grip
                MeshBuilder.add_box(bm, (sx, 0.01, cradle_z + 0.45), (0.045, 0.07, 0.18), m_stock, f"weapon_grip_{s_idx}")

        # 4. Horizontal Locking Retainer Bar with Padlock
        if config.is_locked:
            lock_bar_z = barrel_z - 0.08
            lock_bar_y = 0.08
            # Steel locking pipe spanning all guns
            MeshBuilder.add_cylinder(bm, (0, lock_bar_y, lock_bar_z), 0.02, w - 0.04, sides=6, axis='X', mat_idx=m_steel, name="locking_crossbar")
            # Padlock on left hinge
            MeshBuilder.add_box(bm, (w / 2 - 0.10, lock_bar_y + 0.02, lock_bar_z - 0.03), (0.05, 0.03, 0.06), m_lock, "padlock_body")
            MeshBuilder.add_cylinder(bm, (w / 2 - 0.10, lock_bar_y + 0.02, lock_bar_z), 0.015, 0.01, sides=6, mat_idx=m_steel, name="padlock_loop")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
