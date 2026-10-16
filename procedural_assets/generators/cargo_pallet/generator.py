import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import CargoPalletConfig

class CargoPalletGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for industrial 4-way logistics cargo pallets.
    Builds bottom skid runners, 9-block riser columns, upper deck slats or solid plates,
    fork entry chamfers, tie-down ratchet straps, and optional stacked cargo payload boxes.
    """

    def generate(self, config: CargoPalletConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = CargoPalletConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        l = self.config.length
        w = self.config.width
        h = self.config.height
        half_l = l * 0.5
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        wood_polymer_rgba = (0.28, 0.25, 0.22, 1.0)
        crate_rgba = (0.45, 0.40, 0.32, 1.0)
        strap_rgba = (0.95, 0.75, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Bottom Runner Skids (3 boards in Y)
        # -------------------------------------------------------------
        skid_th = 0.022
        skid_w = 0.12
        for sx in (-half_w + skid_w * 0.5, 0.0, half_w - skid_w * 0.5):
            MeshBuilder.add_box(
                bm,
                size=(skid_w, l, skid_th),
                offset=(sx, 0.0, skid_th * 0.5),
                mat_idx=casing_mat,
                rgba=wood_polymer_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 2. Nine Riser Bearing Blocks (3x3 grid)
        # -------------------------------------------------------------
        block_w = 0.12
        block_l = 0.12
        block_h = h - skid_th * 2 - 0.025
        block_z = skid_th + block_h * 0.5

        is_damaged = (self.config.pallet_condition == "damaged_corner")

        for bx in (-half_w + block_w * 0.5, 0.0, half_w - block_w * 0.5):
            for by in (-half_l + block_l * 0.5, 0.0, half_l - block_l * 0.5):
                # Omit front-left corner block if damaged
                if is_damaged and bx < -half_w * 0.5 and by < -half_l * 0.5:
                    # Broken splinter stump
                    MeshBuilder.add_box(
                        bm,
                        size=(block_w * 0.6, block_l * 0.6, block_h * 0.35),
                        offset=(bx, by, skid_th + block_h * 0.175),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
                    continue

                MeshBuilder.add_box(
                    bm,
                    size=(block_w, block_l, block_h),
                    offset=(bx, by, block_z),
                    mat_idx=casing_mat,
                    rgba=wood_polymer_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 3. Intermediate Stringer Boards (3 boards in Y atop blocks)
        # -------------------------------------------------------------
        stringer_th = 0.022
        stringer_z = skid_th + block_h + stringer_th * 0.5
        for sx in (-half_w + skid_w * 0.5, 0.0, half_w - skid_w * 0.5):
            MeshBuilder.add_box(
                bm,
                size=(skid_w, l, stringer_th),
                offset=(sx, 0.0, stringer_z),
                mat_idx=casing_mat,
                rgba=wood_polymer_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Top Deck Construction
        # -------------------------------------------------------------
        deck_th = 0.022
        deck_z = h - deck_th * 0.5
        style = self.config.deck_style

        if style == "solid_flat":
            MeshBuilder.add_box(
                bm,
                size=(w, l, deck_th),
                offset=(0.0, 0.0, deck_z),
                mat_idx=casing_mat,
                rgba=wood_polymer_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        elif style == "reinforced_steel":
            # Perimeter steel tube frame with cross bracing
            MeshBuilder.add_box(
                bm,
                size=(w, l, deck_th),
                offset=(0.0, 0.0, deck_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Center diamond plate insert
            MeshBuilder.add_box(
                bm,
                size=(w * 0.85, l * 0.85, deck_th * 1.1),
                offset=(0.0, 0.0, deck_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )
        else: # slotted_deck (traditional pallet slats)
            slat_count = 6
            slat_w = 0.11
            slat_spacing = (l - slat_w) / (slat_count - 1)
            for i in range(slat_count):
                sy = -half_l + slat_w * 0.5 + i * slat_spacing
                MeshBuilder.add_box(
                    bm,
                    size=(w, slat_w, deck_th),
                    offset=(0.0, sy, deck_z),
                    mat_idx=casing_mat,
                    rgba=wood_polymer_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 5. Stacked Cargo Payload (Optional)
        # -------------------------------------------------------------
        if self.config.has_cargo_payload:
            # 2 modular shipping boxes stacked on deck
            box1_w = w * 0.45
            box1_l = l * 0.45
            box1_h = 0.50

            # Front-left crate
            MeshBuilder.add_box(
                bm,
                size=(box1_w, box1_l, box1_h),
                offset=(-half_w * 0.45, -half_l * 0.40, h + box1_h * 0.5),
                mat_idx=casing_mat,
                rgba=crate_rgba,
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )
            # Rear-right crate
            MeshBuilder.add_box(
                bm,
                size=(box1_w * 1.1, box1_l * 1.1, box1_h * 1.1),
                offset=(half_w * 0.40, half_l * 0.35, h + box1_h * 0.55),
                mat_idx=metal_mat,
                rgba=(0.35, 0.45, 0.40, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            # Small top supply container
            MeshBuilder.add_box(
                bm,
                size=(box1_w * 0.8, box1_l * 0.8, 0.35),
                offset=(-half_w * 0.35, -half_l * 0.35, h + box1_h + 0.175),
                mat_idx=accent_mat,
                rgba=(0.85, 0.35, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # -------------------------------------------------------------
        # 6. Ratchet Tie-Down Straps (Optional)
        # -------------------------------------------------------------
        if self.config.has_strap_down:
            strap_w = 0.035
            for sx in (-half_w * 0.40, half_w * 0.40):
                # Vertical strap bands across pallet sides
                strap_h = 0.70 if self.config.has_cargo_payload else h
                MeshBuilder.add_box(
                    bm,
                    size=(strap_w, l * 1.02, 0.012),
                    offset=(sx, 0.0, strap_h * 0.5),
                    mat_idx=accent_mat,
                    rgba=strap_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                # Metal ratchet buckle
                MeshBuilder.add_box(
                    bm,
                    size=(0.06, 0.05, 0.035),
                    offset=(sx, half_l * 0.85, strap_h * 0.6),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
