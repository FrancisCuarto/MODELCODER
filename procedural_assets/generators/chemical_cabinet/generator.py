import random
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import ChemicalCabinetConfig

class ChemicalCabinetGenerator(BaseGenerator):
    """Generates PS1 industrial chemical/specimen storage cabinets with glazed framed doors and clutter."""

    def generate(self, config: ChemicalCabinetConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        h = config.height
        d = config.depth

        if config.cabinet_type == "low_counter_top":
            h = min(h, 1.05)
        elif config.cabinet_type == "wall_hanging":
            h = min(h, 0.90)
            d = min(d, 0.35)

        m_casing = mat_mgr.get_material_index("locker_gray")
        m_inner = mat_mgr.get_material_index("casing_inner")
        m_steel = mat_mgr.get_material_index("mounting")
        m_glass = mat_mgr.get_material_index("glass_tube")
        m_hazard = mat_mgr.get_material_index("hazard_yellow")
        m_chem_y = mat_mgr.get_material_index("chemical_barrel_yellow")
        m_chem_b = mat_mgr.get_material_index("chemical_barrel_blue")

        wall_th = 0.035

        # 1. Outer Carcass Box
        # Base plinth / feet (unless wall hanging)
        plinth_h = 0.10 if config.cabinet_type != "wall_hanging" else 0.0
        body_h = h - plinth_h
        body_center_z = plinth_h + body_h / 2

        if plinth_h > 0:
            MeshBuilder.add_box(bm, (0, 0, plinth_h / 2), (w - 0.04, d - 0.04, plinth_h), m_casing, "plinth")

        # Back panel
        MeshBuilder.add_box(bm, (0, -(d / 2 - wall_th / 2), body_center_z), (w, wall_th, body_h), m_inner, "back_wall")
        # Left wall
        MeshBuilder.add_box(bm, (-(w / 2 - wall_th / 2), 0, body_center_z), (wall_th, d, body_h), m_casing, "side_L")
        # Right wall
        MeshBuilder.add_box(bm, ((w / 2 - wall_th / 2), 0, body_center_z), (wall_th, d, body_h), m_casing, "side_R")
        # Top roof
        MeshBuilder.add_box(bm, (0, 0, h - wall_th / 2), (w, d, wall_th), m_casing, "top_roof")
        # Bottom floor
        MeshBuilder.add_box(bm, (0, 0, plinth_h + wall_th / 2), (w, d, wall_th), m_inner, "bottom_floor")

        # 2. Shelves & Chemical Clutter
        shelf_count = 3 if body_h > 1.2 else 2
        shelf_y = 0.0
        shelf_w = w - (wall_th * 2) - 0.01
        shelf_d = d - wall_th - 0.04
        shelf_spacing = (body_h - 0.10) / (shelf_count + 1)

        shelf_z_list = []
        for s_idx in range(1, shelf_count + 1):
            s_z = plinth_h + (s_idx * shelf_spacing)
            shelf_z_list.append(s_z)
            MeshBuilder.add_box(bm, (0, shelf_y, s_z), (shelf_w, shelf_d, 0.025), m_steel, f"shelf_{s_idx}")

            # Reagent bottles & specimen canisters
            if config.shelf_item_density > 0:
                item_slots = [-shelf_w * 0.35, -shelf_w * 0.12, shelf_w * 0.15, shelf_w * 0.35]
                for x_slot in item_slots:
                    if random.random() < config.shelf_item_density:
                        item_type = random.choice(["tall_bottle", "fat_jar", "beaker"])
                        item_z = s_z + 0.012
                        if item_type == "tall_bottle":
                            b_r, b_h = 0.035, 0.14
                            MeshBuilder.add_cylinder(bm, (x_slot, shelf_y - 0.04, item_z + b_h / 2), b_r, b_h, sides=6, mat_idx=m_chem_y, name="bottle")
                            MeshBuilder.add_cylinder(bm, (x_slot, shelf_y - 0.04, item_z + b_h + 0.015), 0.018, 0.03, sides=4, mat_idx=m_steel, name="cap")
                        elif item_type == "fat_jar":
                            j_r, j_h = 0.05, 0.11
                            MeshBuilder.add_cylinder(bm, (x_slot, shelf_y + 0.02, item_z + j_h / 2), j_r, j_h, sides=6, mat_idx=m_chem_b, name="jar")
                        else:
                            c_w, c_h = 0.07, 0.09
                            MeshBuilder.add_box(bm, (x_slot, shelf_y - 0.02, item_z + c_h / 2), (c_w, c_w, c_h), m_glass, "specimen_canister")

        # 3. Hazard Diamond Placard on top
        if body_h > 1.0:
            MeshBuilder.add_box(bm, (0, d / 2 + 0.005, h - 0.15), (0.16, 0.01, 0.16), m_hazard, "hazard_placard")

        # 4. Glazed Framed Doors
        door_w = (w - wall_th * 2) / 2
        door_h = body_h - 0.04
        door_th = 0.03
        front_y = d / 2 - door_th / 2

        # Left Door
        l_open_ang = math.radians(75.0) if config.door_state == "left_open" else 0.0
        l_hinge = Vector((-(w / 2 - wall_th), d / 2, body_center_z))

        # Build door panel locally, then rotate around hinge
        def build_door_panel(door_name, is_right):
            door_sign = 1 if is_right else -1
            panel_dx = door_w / 2 * door_sign
            # Outer door frame border (top, bottom, left, right)
            f_th = 0.05
            glass_w = door_w - (f_th * 2)
            glass_h = door_h - (f_th * 2)

            MeshBuilder.add_box(bm, (0, 0, 0), (door_w, door_th, door_h), m_casing, f"{door_name}_frame")
            # Inset glass pane
            if config.glass_type != "missing_broken":
                MeshBuilder.add_box(bm, (0, 0.005, 0), (glass_w, 0.012, glass_h), m_glass, f"{door_name}_pane")
            # Door pull handle
            handle_x = (door_w / 2 - 0.04) * (-door_sign)
            MeshBuilder.add_box(bm, (handle_x, door_th / 2 + 0.02, 0), (0.02, 0.04, 0.12), m_steel, f"{door_name}_handle")

        # Position Left door
        l_door_center = Vector((-(door_w / 2 + wall_th / 2), front_y, body_center_z))
        if l_open_ang > 0.01:
            # Rotated around hinge
            l_rot = Matrix.Rotation(-l_open_ang, 4, 'Z')
            # Local offset from hinge
            local_offset = Vector((door_w / 2, 0, 0))
            l_pos = l_hinge + (l_rot @ local_offset)
            build_door_panel("door_L", is_right=False)
            for v in bm.verts:
                if v.select:
                    v.co = l_rot @ v.co + l_pos
        else:
            build_door_panel("door_L", is_right=False)
            for v in bm.verts:
                if v.select:
                    v.co += l_door_center

        # Right Door
        r_open_ang = math.radians(25.0) if config.door_state == "right_ajar" else 0.0
        r_door_center = Vector(((door_w / 2 + wall_th / 2), front_y, body_center_z))
        r_hinge = Vector(((w / 2 - wall_th), d / 2, body_center_z))

        if r_open_ang > 0.01:
            r_rot = Matrix.Rotation(r_open_ang, 4, 'Z')
            local_offset = Vector((-door_w / 2, 0, 0))
            r_pos = r_hinge + (r_rot @ local_offset)
            build_door_panel("door_R", is_right=True)
            for v in bm.verts:
                if v.select:
                    v.co = r_rot @ v.co + r_pos
        else:
            build_door_panel("door_R", is_right=True)
            for v in bm.verts:
                if v.select:
                    v.co += r_door_center

        # 5. Heavy Padlock and Hasp
        if config.has_padlock and config.door_state == "both_closed":
            hasp_z = body_center_z
            MeshBuilder.add_box(bm, (0, front_y + door_th / 2 + 0.01, hasp_z), (0.08, 0.02, 0.04), m_steel, "hasp_plate")
            # Padlock body
            MeshBuilder.add_box(bm, (0, front_y + door_th / 2 + 0.03, hasp_z - 0.04), (0.045, 0.025, 0.05), m_casing, "padlock_body")
            # Shackle loop
            MeshBuilder.add_cylinder(bm, (0, front_y + door_th / 2 + 0.03, hasp_z - 0.01), 0.018, 0.01, sides=6, mat_idx=m_steel, name="shackle")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
