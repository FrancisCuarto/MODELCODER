import bpy
import bmesh
import math
from mathutils import Vector, Matrix
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ForkliftCartConfig

class ForkliftCartGenerator(BaseAssetGenerator):
    """
    Procedural generator for manual hydraulic pallet jacks / forklift carts.
    Builds tapered load forks with front tandem rollers, rear hydraulic pump tower,
    dual steering wheels, and angled control tiller handle with release lever.
    """

    def generate(self, config: ForkliftCartConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = ForkliftCartConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        yellow_rgba = (0.95, 0.82, 0.15, 1.0)
        black_rgba = (0.15, 0.15, 0.16, 1.0)

        fork_l = max(0.8, self.config.fork_length)
        fork_w = 0.15
        spread = max(0.4, self.config.fork_spread)
        fork_z = max(0.085, self.config.fork_height)
        fork_thick = 0.05
        half_gap = (spread - (fork_w * 2.0)) * 0.5
        fork_x_left = -half_gap - (fork_w * 0.5)
        fork_x_right = half_gap + (fork_w * 0.5)

        # -------------------------------------------------------------
        # 1. Twin Load Forks (Extending along +Y)
        # -------------------------------------------------------------
        for fx in (fork_x_left, fork_x_right):
            # Main straight blade
            blade_l = fork_l - 0.12
            MeshBuilder.add_box(
                bm,
                size=(fork_w, blade_l, fork_thick),
                offset=(fx, blade_l * 0.5, fork_z),
                mat_idx=accent_mat,
                rgba=yellow_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            # Tapered tip wedge at front
            MeshBuilder.add_box(
                bm,
                size=(fork_w, 0.12, fork_thick * 0.6),
                offset=(fx, blade_l + 0.06, fork_z - (fork_thick * 0.2)),
                mat_idx=accent_mat,
                rgba=yellow_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Front tandem load wheels under tip
            MeshBuilder.add_cylinder(
                bm,
                radius=0.038,
                depth=0.07,
                segments=6,
                offset=(fx, blade_l - 0.05, 0.038),
                axis='X',
                mat_idx=metal_mat,
                rgba=black_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )

        # -------------------------------------------------------------
        # 2. Rear Chassis / Cross Tie Frame
        # -------------------------------------------------------------
        chassis_w = spread + 0.04
        MeshBuilder.add_box(
            bm,
            size=(chassis_w, 0.14, fork_thick * 1.5),
            offset=(0.0, -0.05, fork_z + 0.02),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )

        # Optional vertical load backrest guard
        if self.config.has_load_backrest:
            guard_h = 0.65
            # Left & right vertical uprights
            for gx in (-spread * 0.45, spread * 0.45):
                MeshBuilder.add_box(
                    bm,
                    size=(0.04, 0.04, guard_h),
                    offset=(gx, -0.05, fork_z + (guard_h * 0.5)),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
            # Horizontal cross slats
            for hi in (0.35, 0.65, 0.95):
                MeshBuilder.add_box(
                    bm,
                    size=(spread * 0.95, 0.02, 0.035),
                    offset=(0.0, -0.05, fork_z + (guard_h * hi * 0.95)),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 3. Hydraulic Pump Unit & Steer Head
        # -------------------------------------------------------------
        pump_y = -0.18
        # Steer base block
        MeshBuilder.add_box(
            bm,
            size=(0.22, 0.18, 0.12),
            offset=(0.0, pump_y, 0.14),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Vertical hydraulic cylinder ram
        MeshBuilder.add_cylinder(
            bm,
            radius=0.055,
            depth=0.28,
            segments=7,
            offset=(0.0, pump_y, 0.28),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )
        # Twin steer wheels underneath
        for wx in (-0.08, 0.08):
            MeshBuilder.add_cylinder(
                bm,
                radius=0.085,
                depth=0.05,
                segments=7,
                offset=(wx, pump_y, 0.085),
                axis='X',
                mat_idx=metal_mat,
                rgba=black_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )

        # -------------------------------------------------------------
        # 4. Tiller Arm and Handle (Tilted backwards along -Y)
        # -------------------------------------------------------------
        tiller_pivot_z = 0.40
        tiller_len = 0.82
        t_rad = math.radians(self.config.tiller_angle)

        # Calculate handle position based on angle
        arm_dy = -math.sin(t_rad) * tiller_len
        arm_dz = math.cos(t_rad) * tiller_len
        arm_mid_y = pump_y + (arm_dy * 0.5)
        arm_mid_z = tiller_pivot_z + (arm_dz * 0.5)

        # Tiller main stem box (angled using transform matrix)
        tiller_stem = MeshBuilder.add_box(
            bm,
            size=(0.045, 0.04, tiller_len),
            offset=(0.0, 0.0, 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        rot_mat = Matrix.Rotation(-t_rad, 4, 'X')
        trans_mat = Matrix.Translation(Vector((0.0, arm_mid_y, arm_mid_z)))
        tiller_verts = list({v for f in tiller_stem for v in f.verts})
        bmesh.ops.transform(bm, matrix=trans_mat @ rot_mat, verts=tiller_verts)

        # Handle top head (D-loop grip) at end of tiller arm
        end_y = pump_y + arm_dy
        end_z = tiller_pivot_z + arm_dz

        # Transverse handle grip bar
        MeshBuilder.add_box(
            bm,
            size=(0.32, 0.04, 0.04),
            offset=(0.0, end_y, end_z),
            mat_idx=accent_mat,
            rgba=black_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
        )
        # Side loops
        for hx in (-0.14, 0.14):
            MeshBuilder.add_box(
                bm,
                size=(0.03, 0.12, 0.03),
                offset=(hx, end_y - 0.04, end_z - 0.03),
                mat_idx=accent_mat,
                rgba=yellow_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
        # Hydraulic release trigger lever on handle
        MeshBuilder.add_box(
            bm,
            size=(0.02, 0.08, 0.015),
            offset=(0.06, end_y - 0.03, end_z - 0.01),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
