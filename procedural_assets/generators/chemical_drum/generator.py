import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ChemicalDrumConfig

class ChemicalDrumGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for 55-gallon industrial chemical barrels.
    Features rolled reinforcement chimes, circumferential rolling hoops,
    recessed top head, threaded bung plugs, hazard placards, and optional spill residue.
    """

    def generate(self, config: ChemicalDrumConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = ChemicalDrumConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        radius = self.config.diameter * 0.5
        h = self.config.height
        segments = 8

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        accent_rgba = self.material_manager.get_rgba("accent")

        # Color mapping based on hazard_type
        htype = self.config.hazard_type
        if htype == "flammable":
            body_uv = "red_paint_worn"
            placard_uv = "caution_label"
        elif htype == "toxic":
            body_uv = "hazard_stripes"
            placard_uv = "hazard_stripes"
        elif htype == "coolant":
            body_uv = "painted_metal_white"
            placard_uv = "oxygen_cyan_glow"
        else: # corrosive
            body_uv = "metal_dark_grime"
            placard_uv = "caution_label"

        # -------------------------------------------------------------
        # 1. Main Drum Cylinder Body
        # -------------------------------------------------------------
        MeshBuilder.add_cylinder(
            bm,
            radius=radius,
            depth=h - 0.04,
            segments=segments,
            offset=(0.0, 0.0, h * 0.5),
            axis='Z',
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect(body_uv)
        )

        # -------------------------------------------------------------
        # 2. Top and Bottom Chime Rims (Flanged Seams)
        # -------------------------------------------------------------
        chime_th = 0.035
        chime_r = radius * 1.04

        # Bottom chime
        MeshBuilder.add_cylinder(
            bm,
            radius=chime_r,
            depth=chime_th,
            segments=segments,
            offset=(0.0, 0.0, chime_th * 0.5),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Top chime
        MeshBuilder.add_cylinder(
            bm,
            radius=chime_r,
            depth=chime_th,
            segments=segments,
            offset=(0.0, 0.0, h - chime_th * 0.5),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Recessed top head plate
        MeshBuilder.add_cylinder(
            bm,
            radius=radius * 0.96,
            depth=0.015,
            segments=segments,
            offset=(0.0, 0.0, h - chime_th),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 3. Rolling Hoops / Circumferential Reinforcement Ribs
        # -------------------------------------------------------------
        rib_count = max(1, min(self.config.rib_count, 3))
        rib_th = 0.035
        rib_r = radius * 1.035

        if rib_count == 1:
            rib_zs = [h * 0.5]
        elif rib_count == 2:
            rib_zs = [h * 0.35, h * 0.65]
        else:
            rib_zs = [h * 0.28, h * 0.50, h * 0.72]

        for rz in rib_zs:
            MeshBuilder.add_cylinder(
                bm,
                radius=rib_r,
                depth=rib_th,
                segments=segments,
                offset=(0.0, 0.0, rz),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 4. Threaded Bung Plugs
        # -------------------------------------------------------------
        if self.config.has_bung_caps:
            top_z = h - chime_th + 0.0075
            # 2" Main bung plug
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=0.02,
                segments=6,
                offset=(-radius * 0.45, 0.0, top_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # 3/4" Vent bung plug
            MeshBuilder.add_cylinder(
                bm,
                radius=0.022,
                depth=0.02,
                segments=6,
                offset=(radius * 0.45, 0.0, top_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 5. Chemical Spill / Corrosive Residue (Optional)
        # -------------------------------------------------------------
        if self.config.has_spill_residue:
            # Puddle ring on top head
            MeshBuilder.add_cylinder(
                bm,
                radius=0.07,
                depth=0.005,
                segments=6,
                offset=(-radius * 0.45, 0.0, h - chime_th + 0.015),
                axis='Z',
                mat_idx=accent_mat,
                rgba=(0.3, 0.85, 0.2, 0.85),
                uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
            )
            # Chemical streak dripping down flank
            MeshBuilder.add_box(
                bm,
                size=(0.08, 0.015, 0.35),
                offset=(-radius * 0.45, -radius - 0.005, h * 0.65),
                mat_idx=accent_mat,
                rgba=(0.3, 0.85, 0.2, 0.85),
                uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
            )

        # -------------------------------------------------------------
        # 6. Front Hazard Placard
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(0.20, 0.012, 0.20),
            offset=(0.0, -radius - 0.005, h * 0.5),
            mat_idx=accent_mat,
            rgba=accent_rgba,
            uv_rect=PS1TextureAtlas.get_rect(placard_uv)
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
