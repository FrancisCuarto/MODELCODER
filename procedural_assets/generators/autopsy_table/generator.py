import random
import math
import bpy
import bmesh
from mathutils import Vector

from ...core.base_generator import BaseGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.materials import MaterialManager
from .config import AutopsyTableConfig

class AutopsyTableGenerator(BaseGenerator):
    """Generates PS1 industrial stainless-steel autopsy, dissection, and morgue examination slabs."""

    def generate(self, config: AutopsyTableConfig) -> bpy.types.Object:
        random.seed(config.seed)

        obj, bm = self.create_mesh_object(config.name)
        mat_mgr = self.get_material_manager(config)

        w = config.width
        length = config.length
        h = config.height

        # Materials
        m_steel = mat_mgr.get_material_index("mounting")
        m_dark = mat_mgr.get_material_index("casing")
        m_hose = mat_mgr.get_material_index("cable_black")
        m_lamp = mat_mgr.get_material_index("fluorescent_tube_lit")
        m_stain = mat_mgr.get_material_index("rust_patch")
        m_strap = mat_mgr.get_material_index("chair_vinyl")

        # 1. Base pedestal or tubular legs
        if config.table_type == "quarantine_slab":
            # Heavy central concrete/metal monolith pedestal
            ped_w, ped_l, ped_h = w * 0.55, length * 0.60, h - 0.12
            MeshBuilder.add_box(bm, (0, 0, ped_h / 2), (ped_w, ped_l, ped_h), m_dark, "pedestal")
            # Flange foot
            MeshBuilder.add_box(bm, (0, 0, 0.03), (ped_w + 0.12, ped_l + 0.12, 0.06), m_steel, "pedestal_foot")
        else:
            # 4 Heavy cylindrical or square stainless tubular legs
            leg_r = 0.04
            leg_h = h - 0.10
            x_off = (w / 2) - 0.08
            y_off = (length / 2) - 0.12
            for lx in (-x_off, x_off):
                for ly in (-y_off, y_off):
                    MeshBuilder.add_cylinder(bm, (lx, ly, leg_h / 2), leg_r, leg_h, sides=6, mat_idx=m_steel, name="leg")
                    # Flange foot pad
                    MeshBuilder.add_cylinder(bm, (lx, ly, 0.02), leg_r + 0.03, 0.04, sides=6, mat_idx=m_dark, name="foot_pad")

            # Lower reinforcement crossbars
            MeshBuilder.add_box(bm, (0, -y_off, 0.18), (w - 0.16, 0.04, 0.04), m_steel, "crossbar_y1")
            MeshBuilder.add_box(bm, (0, y_off, 0.18), (w - 0.16, 0.04, 0.04), m_steel, "crossbar_y2")
            MeshBuilder.add_box(bm, (0, 0, 0.18), (0.04, length - 0.24, 0.04), m_steel, "crossbar_center")

        # 2. Main Dissection Surface & Perimeter Drain Lip
        top_z = h - 0.05
        slab_thick = 0.10
        # Main sub-frame
        MeshBuilder.add_box(bm, (0, 0, top_z), (w, length, slab_thick), m_steel, "slab_body")

        # Perimeter retaining trough lips
        lip_h = 0.06
        lip_th = 0.035
        # Side rims
        MeshBuilder.add_box(bm, (-(w / 2 - lip_th / 2), 0, top_z + slab_thick / 2 + lip_h / 2), (lip_th, length, lip_h), m_steel, "rim_left")
        MeshBuilder.add_box(bm, ((w / 2 - lip_th / 2), 0, top_z + slab_thick / 2 + lip_h / 2), (lip_th, length, lip_h), m_steel, "rim_right")
        # End rims
        MeshBuilder.add_box(bm, (0, -(length / 2 - lip_th / 2), top_z + slab_thick / 2 + lip_h / 2), (w - lip_th * 2, lip_th, lip_h), m_steel, "rim_bottom")
        MeshBuilder.add_box(bm, (0, (length / 2 - lip_th / 2), top_z + slab_thick / 2 + lip_h / 2), (w - lip_th * 2, lip_th, lip_h), m_steel, "rim_top")

        # Raised headrest wedge
        head_w = w * 0.45
        head_l = 0.28
        head_h = 0.06
        MeshBuilder.add_box(bm, (0, (length / 2) - 0.20, top_z + slab_thick / 2 + head_h / 2), (head_w, head_l, head_h), m_steel, "headrest_block")

        # 3. Drainage Channel & Suction Pipe
        if config.drainage_channel:
            # Central recessed drain basin
            drain_z = top_z + slab_thick / 2 + 0.005
            MeshBuilder.add_cylinder(bm, (0, -0.20, drain_z), 0.07, 0.015, sides=8, mat_idx=m_dark, name="drain_grate")
            # Drain pipe under the table
            MeshBuilder.add_cylinder(bm, (0, -0.20, top_z - 0.15), 0.03, 0.20, sides=6, mat_idx=m_hose, name="drain_pipe")
            # Collection canister / bucket underneath
            MeshBuilder.add_cylinder(bm, (0, -0.20, 0.16), 0.14, 0.28, sides=8, mat_idx=m_dark, name="waste_bucket")

        # 4. Fluid staining (PSX biological grime patch)
        if config.fluid_stain:
            stain_w = w * 0.48
            stain_l = length * 0.45
            MeshBuilder.add_box(bm, (0.02, -0.05, top_z + slab_thick / 2 + 0.002), (stain_w, stain_l, 0.002), m_stain, "biological_stain")

        # 5. Restraint Straps
        if config.restraint_straps in ("buckled", "torn"):
            strap_y_positions = [-0.60, 0.0, 0.50]
            for sy in strap_y_positions:
                strap_w = w + 0.02
                if config.restraint_straps == "buckled":
                    MeshBuilder.add_box(bm, (0, sy, top_z + slab_thick / 2 + 0.01), (strap_w, 0.05, 0.015), m_strap, "strap")
                    # Buckle in center
                    MeshBuilder.add_box(bm, (0, sy, top_z + slab_thick / 2 + 0.02), (0.06, 0.06, 0.01), m_steel, "buckle")
                else: # torn
                    # Left side hanging
                    MeshBuilder.add_box(bm, (-w / 3, sy, top_z + slab_thick / 2 + 0.01), (w / 3, 0.05, 0.015), m_strap, "strap_left")
                    # Right side ripped down
                    MeshBuilder.add_box(bm, (w / 2 + 0.01, sy, top_z - 0.10), (0.015, 0.05, 0.24), m_strap, "strap_hanging")

        # 6. Overhead Articulated Surgical Examination Lamp
        if config.overhead_lamp:
            lamp_base_x = (w / 2) - 0.05
            lamp_base_y = (length / 2) - 0.10
            # Upright stalk
            MeshBuilder.add_cylinder(bm, (lamp_base_x, lamp_base_y, h + 0.35), 0.025, 0.70, sides=6, mat_idx=m_steel, name="lamp_stalk")
            # Cantilever arm extending toward center
            arm_start = Vector((lamp_base_x, lamp_base_y, h + 0.70))
            arm_end = Vector((0.0, (length / 2) - 0.45, h + 0.85))
            cable_pts = [arm_start, arm_end]
            MeshBuilder.add_extruded_cable(bm, cable_pts, radius=0.02, sides=4, mat_idx=m_steel, name="lamp_arm")
            # Conical spotlight lamp head
            MeshBuilder.add_cylinder(bm, (0.0, (length / 2) - 0.45, h + 0.82), 0.16, 0.08, sides=8, mat_idx=m_steel, name="lamp_shade")
            MeshBuilder.add_cylinder(bm, (0.0, (length / 2) - 0.45, h + 0.77), 0.13, 0.02, sides=8, mat_idx=m_lamp, name="lamp_bulb")

        # 7. Cantilever Instrument Tray & Bone Saw
        if getattr(config, "has_instrument_tray", False):
            tray_x = -(w / 2) - 0.14
            tray_y = 0.20
            arm_pts = [
                Vector((-(w / 2) + 0.04, tray_y, h - 0.15)),
                Vector((tray_x, tray_y, h - 0.05)),
                Vector((tray_x, tray_y, h + 0.08))
            ]
            MeshBuilder.add_extruded_cable(bm, arm_pts, radius=0.018, sides=4, mat_idx=m_steel, name="tray_arm")
            MeshBuilder.add_box(bm, (tray_x, tray_y, h + 0.09), (0.28, 0.40, 0.02), m_steel, "instrument_tray")
            MeshBuilder.add_box(bm, (tray_x - 0.04, tray_y, h + 0.105), (0.02, 0.22, 0.01), m_dark, "saw_handle")
            MeshBuilder.add_box(bm, (tray_x + 0.02, tray_y, h + 0.105), (0.015, 0.18, 0.008), m_steel, "blade")

        # 8. Glass Quarantine Specimen Jars
        jars = getattr(config, "specimen_jar_count", 0)
        if jars > 0:
            m_glass = mat_mgr.get_material_index("glass_tube")
            m_fluid = mat_mgr.get_material_index("oxygen_cyan")
            jar_xs = [-0.15, 0.0, 0.15]
            for j in range(min(3, jars)):
                jx = jar_xs[j]
                jy = -(length / 2) + 0.25
                jz = 0.22
                MeshBuilder.add_cylinder(bm, (jx, jy, jz), 0.04, 0.12, sides=6, mat_idx=m_glass, name="specimen_jar")
                MeshBuilder.add_cylinder(bm, (jx, jy, jz), 0.035, 0.08, sides=6, mat_idx=m_fluid, name="jar_fluid")
                MeshBuilder.add_cylinder(bm, (jx, jy, jz + 0.065), 0.042, 0.015, sides=6, mat_idx=m_dark, name="jar_lid")

        mat_mgr.assign_to_mesh(obj)
        self.finalize_mesh(obj, bm)
        return obj
