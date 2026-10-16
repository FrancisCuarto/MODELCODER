import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ConveyorSegmentConfig

class ConveyorSegmentGenerator(BaseAssetGenerator):
    """
    Procedural generator for modular industrial conveyor segments.
    Builds structural C-channel side frames, free or driven rollers, support legs with foot pads,
    drive motor gearbox pod, and safety guide rails.
    """

    def generate(self, config: ConveyorSegmentConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = ConveyorSegmentConfig()

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
        yellow_rgba = (0.95, 0.85, 0.20, 1.0)
        red_rgba = (0.90, 0.15, 0.15, 1.0)

        length = max(1.0, self.config.length)
        width = max(0.5, self.config.width)
        height = max(0.4, self.config.height)
        half_l = length * 0.5
        half_w = width * 0.5

        incline_rad = math.radians(self.config.incline_angle)
        z_delta = half_l * math.sin(incline_rad)

        # -------------------------------------------------------------
        # 1. Longitudinal Side C-Channel Beams (Left & Right)
        # -------------------------------------------------------------
        beam_h = 0.12
        beam_t = 0.04
        for sx in (-half_w, half_w):
            MeshBuilder.add_box(
                bm,
                size=(beam_t, length, beam_h),
                offset=(sx, 0.0, height),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # End cap plates
            for sy in (-half_l, half_l):
                MeshBuilder.add_box(
                    bm,
                    size=(beam_t * 1.3, 0.03, beam_h * 1.1),
                    offset=(sx, sy, height),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 2. Rollers or Continuous Belt Surface
        # -------------------------------------------------------------
        inner_w = width - (beam_t * 2.0)
        roller_count = max(4, self.config.roller_density)
        y_step = (length - 0.20) / max(1, roller_count - 1)

        if self.config.conveyor_type == "belt":
            # Flat top belt sheet
            MeshBuilder.add_box(
                bm,
                size=(inner_w, length - 0.08, 0.02),
                offset=(0.0, 0.0, height + (beam_h * 0.3)),
                mat_idx=metal_mat,
                rgba=(0.18, 0.18, 0.20, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )
            # Front and rear crown drive drums
            for dy in (-half_l + 0.06, half_l - 0.06):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.045,
                    depth=inner_w,
                    segments=6,
                    offset=(0.0, dy, height + 0.02),
                    axis='X',
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
        else:
            # Roller array along Y axis
            for i in range(roller_count):
                ry = -half_l + 0.10 + (i * y_step)
                rz = height + (beam_h * 0.25)
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.032,
                    depth=inner_w,
                    segments=6,
                    offset=(0.0, ry, rz),
                    axis='X',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        # -------------------------------------------------------------
        # 3. Support Legs with Foot Pads and Cross Ties
        # -------------------------------------------------------------
        leg_inset = min(0.35, length * 0.22)
        leg_pairs_y = [-half_l + leg_inset, half_l - leg_inset]
        if length > 2.6:
            leg_pairs_y.append(0.0)

        leg_size = 0.05
        pad_size = 0.12

        for ly in leg_pairs_y:
            for lx in (-half_w, half_w):
                leg_h = height - (beam_h * 0.5)
                # Vertical leg post
                MeshBuilder.add_box(
                    bm,
                    size=(leg_size, leg_size, leg_h),
                    offset=(lx, ly, leg_h * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Base foot pad
                MeshBuilder.add_box(
                    bm,
                    size=(pad_size, pad_size, 0.015),
                    offset=(lx, ly, 0.0075),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                )
            # Transverse cross brace between left and right leg
            cross_z = (height - (beam_h * 0.5)) * 0.4
            MeshBuilder.add_box(
                bm,
                size=(width, leg_size * 0.8, 0.03),
                offset=(0.0, ly, cross_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Side Guide Rails (Optional)
        # -------------------------------------------------------------
        if self.config.has_side_rails:
            rail_z = height + beam_h + 0.06
            for rx in (-half_w - 0.015, half_w + 0.015):
                # Longitudinal top rail bar
                MeshBuilder.add_box(
                    bm,
                    size=(0.02, length, 0.03),
                    offset=(rx, 0.0, rail_z),
                    mat_idx=accent_mat,
                    rgba=yellow_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                # Vertical stanchions
                stanchion_count = 3 if length < 2.5 else 4
                s_step = (length - 0.2) / max(1, stanchion_count - 1)
                for si in range(stanchion_count):
                    sy = -half_l + 0.1 + (si * s_step)
                    MeshBuilder.add_box(
                        bm,
                        size=(0.015, 0.02, beam_h + 0.06),
                        offset=(rx, sy, height + (beam_h * 0.5) + 0.03),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        # -------------------------------------------------------------
        # 5. Electric Drive Motor Box (Optional)
        # -------------------------------------------------------------
        if self.config.has_motor:
            motor_x = half_w + 0.14
            motor_y = half_l - 0.35
            motor_z = height - 0.06

            # Main gearbox housing
            MeshBuilder.add_box(
                bm,
                size=(0.18, 0.26, 0.18),
                offset=(motor_x, motor_y, motor_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_vent_grate")
            )
            # Cylindrical stator motor bell
            MeshBuilder.add_cylinder(
                bm,
                radius=0.07,
                depth=0.14,
                segments=6,
                offset=(motor_x, motor_y - 0.18, motor_z),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Drive chain shroud connecting motor to side beam
            MeshBuilder.add_box(
                bm,
                size=(0.12, 0.10, 0.14),
                offset=(half_w + 0.06, motor_y, height),
                mat_idx=accent_mat,
                rgba=yellow_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # -------------------------------------------------------------
        # 6. Emergency Stop Switch Box
        # -------------------------------------------------------------
        e_x = -half_w - 0.05
        e_y = -half_l + 0.35
        e_z = height - 0.05
        MeshBuilder.add_box(
            bm,
            size=(0.06, 0.08, 0.10),
            offset=(e_x, e_y, e_z),
            mat_idx=accent_mat,
            rgba=red_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )
        # Push mushroom button
        MeshBuilder.add_cylinder(
            bm,
            radius=0.02,
            depth=0.03,
            segments=5,
            offset=(e_x - 0.03, e_y, e_z),
            axis='X',
            mat_idx=accent_mat,
            rgba=yellow_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
