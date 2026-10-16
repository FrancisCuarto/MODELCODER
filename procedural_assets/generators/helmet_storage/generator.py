import math
import hashlib
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import HelmetStorageConfig

class HelmetStorageGenerator(BaseAssetGenerator[HelmetStorageConfig]):
    """
    Procedural generator for Helmet Storage:
    Modular compartmentalized locker unit for EVA spacesuit helmets,
    with charging stations, status LEDs, and locking latch cubbies.
    """

    def generate(self, config: HelmetStorageConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.width
        h = self.config.height
        d = self.config.depth

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        glass_mat = m_idx.get("glass", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        brass_rgba = (0.85, 0.68, 0.22, 1.0)

        # 1. Main outer cabinet shell
        wall_t = 0.05
        base_h = 0.10

        # Base plinth
        MeshBuilder.add_box(
            bm,
            size=(w, d, base_h),
            offset=(0.0, 0.0, base_h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        inner_h = h - base_h - wall_t
        inner_z = base_h + inner_h / 2.0

        # Rear back wall
        MeshBuilder.add_box(
            bm,
            size=(w, wall_t, inner_h),
            offset=(0.0, -d / 2.0 + wall_t / 2.0, inner_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top cap
        MeshBuilder.add_box(
            bm,
            size=(w, d, wall_t),
            offset=(0.0, 0.0, h - wall_t / 2.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Left and Right side panels
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(wall_t, d - wall_t, inner_h),
                offset=(sx * (w / 2.0 - wall_t / 2.0), wall_t / 2.0, inner_z),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

        # 2. Grid compartments (rows and columns)
        rows = max(2, min(4, int(self.config.grid_rows)))
        cols = max(1, min(3, int(self.config.grid_cols)))

        inner_w = w - 2.0 * wall_t
        inner_d = d - wall_t

        col_w = inner_w / float(cols)
        row_h = inner_h / float(rows)

        # Vertical dividers
        for c in range(1, cols):
            div_x = -inner_w / 2.0 + c * col_w
            MeshBuilder.add_box(
                bm,
                size=(wall_t * 0.6, inner_d, inner_h),
                offset=(div_x, wall_t / 2.0, inner_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Horizontal shelf dividers
        for r in range(1, rows):
            div_z = base_h + r * row_h
            MeshBuilder.add_box(
                bm,
                size=(inner_w, inner_d, wall_t * 0.6),
                offset=(0.0, wall_t / 2.0, div_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # 3. Cubby contents (Helmet and charging dock)
        for r in range(rows):
            cubby_z = base_h + r * row_h + row_h / 2.0
            shelf_floor_z = base_h + r * row_h

            for c in range(cols):
                cubby_x = -inner_w / 2.0 + c * col_w + col_w / 2.0
                slot_key = f"{self.config.seed}_{r}_{c}"
                h_val = int(hashlib.md5(slot_key.encode()).hexdigest()[:4], 16) / 65535.0
                has_helmet = h_val <= self.config.helmet_density

                # Charging ring dock on the shelf
                MeshBuilder.add_cylinder(
                    bm,
                    radius=min(col_w, inner_d) * 0.28,
                    depth=0.03,
                    segments=8,
                    offset=(cubby_x, 0.05, shelf_floor_z + 0.02),
                    axis='Z',
                    mat_idx=metal_mat,
                    rgba=(0.15, 0.15, 0.18, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

                # Status LED indicator above each cubby
                if self.config.has_status_leds:
                    led_rect = PS1TextureAtlas.get_rect("led_green" if has_helmet else "led_yellow")
                    MeshBuilder.add_box(
                        bm,
                        size=(0.02, 0.01, 0.02),
                        offset=(cubby_x, d / 2.0 - 0.02, shelf_floor_z + row_h - 0.03),
                        mat_idx=screen_mat,
                        rgba=(0.2, 0.85, 0.2, 1.0) if has_helmet else (0.9, 0.75, 0.1, 1.0),
                        uv_rect=led_rect
                    )

                if has_helmet:
                    # Low-poly EVA helmet dome
                    h_rad = min(col_w, row_h) * 0.32
                    h_center_z = shelf_floor_z + 0.03 + h_rad
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=h_rad,
                        depth=h_rad * 1.6,
                        segments=8,
                        offset=(cubby_x, 0.04, h_center_z),
                        axis='Z',
                        mat_idx=casing_mat,
                        rgba=(0.92, 0.94, 0.96, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                    )

                    # Gold amber reflective bubble visor
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=h_rad * 0.75,
                        depth=0.06,
                        segments=8,
                        offset=(cubby_x, 0.04 + h_rad * 0.65, h_center_z + h_rad * 0.1),
                        axis='Y',
                        mat_idx=screen_mat,
                        rgba=(0.88, 0.68, 0.2, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                    )

                    # Neck locking collar
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=h_rad * 0.92,
                        depth=0.035,
                        segments=8,
                        offset=(cubby_x, 0.04, shelf_floor_z + 0.04),
                        axis='Z',
                        mat_idx=brass_mat,
                        rgba=brass_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                    )

        # 4. Optional door mesh or glass
        if self.config.door_style == "glass_door":
            MeshBuilder.add_box(
                bm,
                size=(inner_w, 0.015, inner_h),
                offset=(0.0, d / 2.0 - 0.01, inner_z),
                mat_idx=glass_mat,
                rgba=(0.35, 0.65, 0.75, 0.4),
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )
        elif self.config.door_style == "mesh_grate":
            MeshBuilder.add_box(
                bm,
                size=(inner_w, 0.015, inner_h),
                offset=(0.0, d / 2.0 - 0.01, inner_z),
                mat_idx=metal_mat,
                rgba=(0.3, 0.3, 0.35, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
