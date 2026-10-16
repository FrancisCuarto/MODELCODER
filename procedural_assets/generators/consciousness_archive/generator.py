import math
import hashlib
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ConsciousnessArchiveConfig

class ConsciousnessArchiveGenerator(BaseAssetGenerator[ConsciousnessArchiveConfig]):
    """
    Procedural generator for Consciousness Archive:
    Industrial bank of memory cartridge bays with coolant piping, status LEDs,
    and modular memory cassettes storing human neural telemetry.
    """

    def generate(self, config: ConsciousnessArchiveConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.width
        d = self.config.depth
        h = self.config.height

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        brass_rgba = (0.85, 0.65, 0.18, 1.0)

        # 1. Outer heavy rack chassis
        wall_t = 0.08
        base_h = 0.12
        top_h = 0.18

        # Base plinth
        MeshBuilder.add_box(
            bm,
            size=(w, d, base_h),
            offset=(0.0, 0.0, base_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Side upright posts
        shelf_h = h - base_h - top_h
        shelf_center_z = base_h + shelf_h / 2.0
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(wall_t, d, shelf_h),
                offset=(sx * (w / 2.0 - wall_t / 2.0), 0.0, shelf_center_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Back closure panel
        MeshBuilder.add_box(
            bm,
            size=(w - 2.0 * wall_t, wall_t, shelf_h),
            offset=(0.0, -d / 2.0 + wall_t / 2.0, shelf_center_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top exhaust / coolant manifold
        MeshBuilder.add_box(
            bm,
            size=(w, d, top_h),
            offset=(0.0, 0.0, h - top_h / 2.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        if self.config.has_cooling_vent:
            # Vent grill on top manifold face
            MeshBuilder.add_box(
                bm,
                size=(w * 0.75, 0.02, top_h * 0.7),
                offset=(0.0, d / 2.0 + 0.005, h - top_h / 2.0),
                mat_idx=metal_mat,
                rgba=(0.15, 0.15, 0.18, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # 2. Horizontal shelf dividers and memory cartridge bays
        rows = max(2, min(6, int(self.config.bay_rows)))
        row_span = shelf_h / float(rows)
        slots_per_row = 4
        slot_w = (w - 2.0 * wall_t - 0.05) / float(slots_per_row)

        for r in range(rows):
            shelf_z = base_h + r * row_span
            # Shelf divider plate
            MeshBuilder.add_box(
                bm,
                size=(w - 2.0 * wall_t, d - wall_t, 0.03),
                offset=(0.0, 0.0, shelf_z + 0.015),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Cartridge bays in this row
            bay_center_z = shelf_z + row_span / 2.0
            for s in range(slots_per_row):
                # Deterministic check if slot is filled
                slot_key = f"{self.config.seed}_{r}_{s}"
                h_val = int(hashlib.md5(slot_key.encode()).hexdigest()[:4], 16) / 65535.0
                is_filled = h_val <= self.config.cartridge_density

                slot_x = -(w / 2.0 - wall_t - 0.025) + s * slot_w + slot_w / 2.0

                if is_filled:
                    # Cartridge body protruding slightly from bay
                    c_len = d * 0.8
                    MeshBuilder.add_box(
                        bm,
                        size=(slot_w * 0.78, c_len, row_span * 0.65),
                        offset=(slot_x, 0.05, bay_center_z),
                        mat_idx=metal_mat,
                        rgba=(0.25, 0.28, 0.32, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
                    )

                    # Front gold/amber connector handle and status LED
                    MeshBuilder.add_box(
                        bm,
                        size=(slot_w * 0.5, 0.04, row_span * 0.25),
                        offset=(slot_x, d / 2.0 + 0.02, bay_center_z),
                        mat_idx=brass_mat,
                        rgba=brass_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                    )

                    # Status LED (green or amber depending on slot hash)
                    led_rect = PS1TextureAtlas.get_rect("led_green" if (h_val % 0.3 < 0.2) else "led_yellow")
                    MeshBuilder.add_box(
                        bm,
                        size=(0.02, 0.01, 0.02),
                        offset=(slot_x + slot_w * 0.25, d / 2.0 + 0.015, bay_center_z + row_span * 0.2),
                        mat_idx=screen_mat,
                        rgba=(0.2, 0.9, 0.2, 1.0),
                        uv_rect=led_rect
                    )
                else:
                    # Empty bay guide rails
                    MeshBuilder.add_box(
                        bm,
                        size=(slot_w * 0.85, 0.04, 0.02),
                        offset=(slot_x, d / 2.0 - 0.04, bay_center_z - row_span * 0.3),
                        mat_idx=metal_mat,
                        rgba=(0.1, 0.1, 0.12, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        # 3. Conduit wiring harness running along one side
        if self.config.has_conduit_harness:
            harness_x = w / 2.0 + 0.03
            MeshBuilder.add_cylinder(
                bm,
                radius=0.03,
                depth=shelf_h * 0.95,
                segments=6,
                offset=(harness_x, 0.0, shelf_center_z),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.1, 0.1, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )
            # Mounting brackets
            for bz in (base_h + shelf_h * 0.25, base_h + shelf_h * 0.75):
                MeshBuilder.add_box(
                    bm,
                    size=(0.06, 0.08, 0.04),
                    offset=(w / 2.0, 0.0, bz),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
