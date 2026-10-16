import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import FoodStorageUnitConfig

class FoodStorageUnitGenerator(BaseAssetGenerator):
    """
    Procedural generator for crew habitation food and synthetic ration storage cabinets.
    Builds modular tier locker casing, compression lever latches, ventilation louver slots,
    internal ration pack trays, and inventory label plaques.
    """

    def generate(self, config: FoodStorageUnitConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = FoodStorageUnitConfig()

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
        ration_rgba = (0.85, 0.80, 0.65, 1.0)

        w = max(0.6, self.config.width)
        d = max(0.4, self.config.depth)
        h = max(1.2, self.config.height)

        half_w = w * 0.5
        half_d = d * 0.5
        half_h = h * 0.5

        # -------------------------------------------------------------
        # 1. Base Cabinet Box & Plinth
        # -------------------------------------------------------------
        # 4 Corner rubber/steel foot pads
        for fx in (-half_w + 0.05, half_w - 0.05):
            for fy in (-half_d + 0.05, half_d - 0.05):
                MeshBuilder.add_box(
                    bm,
                    size=(0.06, 0.06, 0.04),
                    offset=(fx, fy, 0.02),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                )

        body_h = h - 0.04
        body_z = 0.04 + (body_h * 0.5)

        # Main cabinet housing body
        MeshBuilder.add_box(
            bm,
            size=(w, d, body_h),
            offset=(0.0, 0.0, body_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        front_y = half_d

        # -------------------------------------------------------------
        # 2. Compartment Rows & Door Facades
        # -------------------------------------------------------------
        rows = max(2, self.config.compartment_rows)
        usable_h = body_h - 0.12
        tier_h = usable_h / rows
        start_z = 0.04 + 0.06 + (tier_h * 0.5)

        for ri in range(rows):
            rz = start_z + (ri * tier_h)
            door_w = w * 0.88
            door_h = tier_h - 0.02

            # Looted open state simulation: omit door on top tier
            if self.config.storage_state == "open_looted" and ri == (rows - 1):
                # Recessed open cavity
                MeshBuilder.add_box(
                    bm,
                    size=(door_w, 0.08, door_h),
                    offset=(0.0, front_y - 0.04, rz),
                    mat_idx=metal_mat,
                    rgba=(0.12, 0.12, 0.14, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
                # Scattered ration pack blocks inside
                MeshBuilder.add_box(
                    bm,
                    size=(0.12, 0.14, 0.06),
                    offset=(0.08, front_y - 0.02, rz - (door_h * 0.25)),
                    mat_idx=accent_mat,
                    rgba=ration_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                continue

            # Inset door panel
            MeshBuilder.add_box(
                bm,
                size=(door_w, 0.012, door_h),
                offset=(0.0, front_y + 0.006, rz),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )

            # Compression latch handle
            if self.config.has_latch_bars:
                MeshBuilder.add_box(
                    bm,
                    size=(0.025, 0.02, 0.07),
                    offset=(half_w * 0.68, front_y + 0.018, rz),
                    mat_idx=accent_mat,
                    rgba=(0.95, 0.85, 0.20, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )

            # Identification label slot
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.006, 0.035),
                offset=(-half_w * 0.40, front_y + 0.014, rz),
                mat_idx=casing_mat,
                rgba=(0.90, 0.90, 0.92, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
            )

        # -------------------------------------------------------------
        # 3. Ventilation Louvers (Top & Bottom)
        # -------------------------------------------------------------
        for vz in (0.04 + 0.03, h - 0.03):
            MeshBuilder.add_box(
                bm,
                size=(w * 0.70, 0.008, 0.03),
                offset=(0.0, front_y + 0.004, vz),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_vent_grate")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
