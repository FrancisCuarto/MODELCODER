import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import PowerTransformerConfig

class PowerTransformerGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for high-voltage substation power transformers.
    Features heavy structural skid, corrugated oil tank, side cooling radiator fin banks,
    stepped ceramic high-voltage bushings, top expansion conservator tank, and terminal marshalling box.
    """

    def generate(self, config: PowerTransformerConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = PowerTransformerConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.transformer_width
        d = self.config.transformer_depth
        h = self.config.transformer_height
        half_w = w * 0.5
        half_d = d * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        ceramic_rgba = (0.85, 0.55, 0.25, 1.0)
        brass_rgba = (0.85, 0.70, 0.25, 1.0)

        # -------------------------------------------------------------
        # 1. Base Skid I-Beams & Grounding Lug
        # -------------------------------------------------------------
        skid_h = 0.08
        beam_w = 0.08
        for sy in (-half_d + 0.10, half_d - 0.10):
            MeshBuilder.add_box(
                bm,
                size=(w + 0.10, beam_w, skid_h),
                offset=(0.0, sy, skid_h * 0.5),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Copper grounding terminal lug
        MeshBuilder.add_cylinder(
            bm,
            radius=0.025,
            depth=0.03,
            segments=6,
            offset=(-half_w + 0.04, -half_d + 0.04, skid_h + 0.015),
            axis='Z',
            mat_idx=metal_mat,
            rgba=brass_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 2. Main Oil Tank Body
        # -------------------------------------------------------------
        tank_w = w * 0.65
        tank_d = d * 0.70
        tank_h = h * 0.58
        tank_z = skid_h + tank_h * 0.5

        MeshBuilder.add_box(
            bm,
            size=(tank_w, tank_d, tank_h),
            offset=(0.0, 0.0, tank_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Top tank cover rim flange
        flange_th = 0.035
        MeshBuilder.add_box(
            bm,
            size=(tank_w + 0.06, tank_d + 0.06, flange_th),
            offset=(0.0, 0.0, skid_h + tank_h + flange_th * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Side Radiator Cooling Fin Banks (Left and Right)
        # -------------------------------------------------------------
        if self.config.cooling_radiators_sides:
            rad_w = 0.10
            rad_d = tank_d * 0.85
            rad_h = tank_h * 0.78
            for side in (-1.0, 1.0):
                rx = side * (tank_w * 0.5 + rad_w * 0.5 + 0.02)
                # Radiator header pipes
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.025,
                    depth=rad_d,
                    segments=6,
                    offset=(rx, 0.0, tank_z + rad_h * 0.45),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.025,
                    depth=rad_d,
                    segments=6,
                    offset=(rx, 0.0, tank_z - rad_h * 0.45),
                    axis='Y',
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                # Radiator vertical fin core
                MeshBuilder.add_box(
                    bm,
                    size=(rad_w, rad_d, rad_h),
                    offset=(rx, 0.0, tank_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("vent_grill")
                )

        # -------------------------------------------------------------
        # 4. High-Voltage Stepped Ceramic Bushing Insulators
        # -------------------------------------------------------------
        ins_count = max(2, min(self.config.insulator_count, 4))
        ins_cover_z = skid_h + tank_h + flange_th
        ins_spacing = (tank_w * 0.75) / (ins_count + 1)
        ins_start_x = -tank_w * 0.375 + ins_spacing

        for ii in range(ins_count):
            ix = ins_start_x + ii * ins_spacing
            iy = 0.0
            # Base stepped disc
            MeshBuilder.add_cylinder(
                bm,
                radius=0.055,
                depth=0.04,
                segments=6,
                offset=(ix, iy, ins_cover_z + 0.02),
                axis='Z',
                mat_idx=metal_mat,
                rgba=ceramic_rgba,
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )
            # Middle ribbed cone
            MeshBuilder.add_cylinder(
                bm,
                radius=0.042,
                depth=0.14,
                segments=6,
                offset=(ix, iy, ins_cover_z + 0.11),
                axis='Z',
                mat_idx=metal_mat,
                rgba=ceramic_rgba,
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )
            # Top skirt disc
            MeshBuilder.add_cylinder(
                bm,
                radius=0.050,
                depth=0.03,
                segments=6,
                offset=(ix, iy, ins_cover_z + 0.195),
                axis='Z',
                mat_idx=metal_mat,
                rgba=ceramic_rgba,
                uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
            )
            # Terminal brass bolt stud on top
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.07,
                segments=6,
                offset=(ix, iy, ins_cover_z + 0.245),
                axis='Z',
                mat_idx=metal_mat,
                rgba=brass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 5. Conservator Oil Reservoir Expansion Tank
        # -------------------------------------------------------------
        if self.config.has_expansion_tank:
            tank_cyl_r = 0.09
            tank_cyl_len = tank_w * 0.85
            tank_cyl_z = ins_cover_z + 0.28
            tank_cyl_y = tank_d * 0.28

            # Support stanchions
            for sx in (-tank_w * 0.25, tank_w * 0.25):
                MeshBuilder.add_box(
                    bm,
                    size=(0.03, 0.03, 0.28),
                    offset=(sx, tank_cyl_y, ins_cover_z + 0.14),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

            # Conservator drum
            MeshBuilder.add_cylinder(
                bm,
                radius=tank_cyl_r,
                depth=tank_cyl_len,
                segments=8,
                offset=(0.0, tank_cyl_y, tank_cyl_z),
                axis='X',
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

            # Oil level sight glass
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=tank_cyl_len * 0.5,
                segments=6,
                offset=(0.0, tank_cyl_y - tank_cyl_r, tank_cyl_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=(0.3, 0.7, 0.9, 0.8),
                uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
            )

        # -------------------------------------------------------------
        # 6. Marshalling Box & High-Voltage Warning Placard
        # -------------------------------------------------------------
        box_w = tank_w * 0.45
        box_d = 0.09
        box_h = tank_h * 0.45
        box_y = -tank_d * 0.5 - box_d * 0.5
        box_z = tank_z

        MeshBuilder.add_box(
            bm,
            size=(box_w, box_d, box_h),
            offset=(0.0, box_y, box_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Hazard warning sign
        MeshBuilder.add_box(
            bm,
            size=(box_w * 0.65, 0.012, box_h * 0.55),
            offset=(0.0, box_y - box_d * 0.5 - 0.005, box_z),
            mat_idx=accent_mat,
            rgba=(0.95, 0.85, 0.1, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("caution_label")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
