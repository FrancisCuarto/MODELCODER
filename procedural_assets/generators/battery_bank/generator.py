import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import BatteryBankConfig

class BatteryBankGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial backup battery accumulator banks.
    Features heavy angle-iron rack frame, acid-resistant shelf trays, lead-acid/lithium cells,
    copper series busbar interconnects, digital charge controller terminal, and hazard labels.
    """

    def generate(self, config: BatteryBankConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = BatteryBankConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.rack_width
        d = self.config.rack_depth
        h = self.config.rack_height
        half_w = w * 0.5
        half_d = d * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)
        copper_rgba = (0.85, 0.55, 0.20, 1.0)

        # Status color
        c_state = self.config.charge_state
        if c_state == "nominal":
            screen_uv = "crt_screen_green"
            screen_rgba = (0.2, 0.85, 0.45, 1.0)
        elif c_state == "discharging":
            screen_uv = "crt_screen_amber"
            screen_rgba = (0.95, 0.65, 0.15, 1.0)
        elif c_state == "alarm":
            screen_uv = "crt_screen_amber"
            screen_rgba = (0.95, 0.20, 0.15, 1.0)
        else: # depleted
            screen_uv = "crt_screen_off"
            screen_rgba = (0.2, 0.22, 0.24, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Angle-Iron Rack Frame
        # -------------------------------------------------------------
        post_w = 0.045
        # 4 Corner uprights
        for sx in (-half_w + post_w * 0.5, half_w - post_w * 0.5):
            for sy in (-half_d + post_w * 0.5, half_d - post_w * 0.5):
                MeshBuilder.add_box(
                    bm,
                    size=(post_w, post_w, h),
                    offset=(sx, sy, h * 0.5),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # Bottom floor rails
        for sy in (-half_d + post_w * 0.5, half_d - post_w * 0.5):
            MeshBuilder.add_box(
                bm,
                size=(w, post_w, 0.04),
                offset=(0.0, sy, 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        # Top header tie rails
        for sy in (-half_d + post_w * 0.5, half_d - post_w * 0.5):
            MeshBuilder.add_box(
                bm,
                size=(w, post_w, 0.04),
                offset=(0.0, sy, h - 0.02),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 2. Shelf Trays and Battery Cell Blocks
        # -------------------------------------------------------------
        tiers = max(2, min(self.config.tier_count, 4))
        cells_per_tier = max(2, min(self.config.batteries_per_tier, 5))

        tray_w = w - post_w * 2 - 0.02
        tray_d = d - post_w * 2 - 0.02
        avail_h = h - 0.35
        tier_spacing = avail_h / tiers

        cell_w = (tray_w - 0.08) / cells_per_tier
        cell_d = tray_d * 0.78
        cell_h = min(0.32, tier_spacing * 0.65)

        for ti in range(tiers):
            tier_z = 0.12 + ti * tier_spacing

            # Heavy steel shelf tray with acid lip
            MeshBuilder.add_box(
                bm,
                size=(tray_w, tray_d, 0.035),
                offset=(0.0, 0.0, tier_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

            # Battery cells on this tier
            for ci in range(cells_per_tier):
                cx = -tray_w * 0.5 + 0.04 + ci * cell_w + cell_w * 0.5
                cy = 0.0
                cz = tier_z + 0.0175 + cell_h * 0.5

                # Main battery cell body
                MeshBuilder.add_box(
                    bm,
                    size=(cell_w * 0.90, cell_d, cell_h),
                    offset=(cx, cy, cz),
                    mat_idx=metal_mat,
                    rgba=rubber_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )

                # Positive terminal (+ red)
                MeshBuilder.add_box(
                    bm,
                    size=(0.024, 0.024, 0.03),
                    offset=(cx - cell_w * 0.25, cy - cell_d * 0.25, cz + cell_h * 0.5 + 0.015),
                    mat_idx=accent_mat,
                    rgba=(0.90, 0.15, 0.1, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("button_red")
                )

                # Negative terminal (- black/metal)
                MeshBuilder.add_box(
                    bm,
                    size=(0.024, 0.024, 0.03),
                    offset=(cx + cell_w * 0.25, cy - cell_d * 0.25, cz + cell_h * 0.5 + 0.015),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

                # Series Busbars connecting neighboring cells
                if self.config.has_busbars and ci < cells_per_tier - 1:
                    bus_x = cx + cell_w * 0.5
                    bus_y = cy - cell_d * 0.25
                    bus_z = cz + cell_h * 0.5 + 0.03
                    MeshBuilder.add_box(
                        bm,
                        size=(cell_w * 0.55, 0.015, 0.008),
                        offset=(bus_x, bus_y, bus_z),
                        mat_idx=metal_mat,
                        rgba=copper_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                    )

        # -------------------------------------------------------------
        # 3. Top Digital Charge Controller Monitor
        # -------------------------------------------------------------
        if self.config.has_charge_monitor:
            mon_w = w * 0.40
            mon_h = 0.18
            mon_d = 0.12
            mon_z = h - 0.12

            # Monitor chassis
            MeshBuilder.add_box(
                bm,
                size=(mon_w, mon_d, mon_h),
                offset=(0.0, -half_d + 0.06, mon_z),
                mat_idx=casing_mat,
                rgba=(0.78, 0.76, 0.72, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )

            # Telemetry screen
            MeshBuilder.add_box(
                bm,
                size=(mon_w * 0.65, 0.015, mon_h * 0.55),
                offset=(0.0, -half_d - 0.005, mon_z),
                mat_idx=screen_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect(screen_uv)
            )

            # High voltage DC caution placard
            MeshBuilder.add_box(
                bm,
                size=(0.22, 0.01, 0.14),
                offset=(half_w * 0.55, -half_d - 0.005, mon_z),
                mat_idx=accent_mat,
                rgba=(0.95, 0.85, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("caution_label")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
