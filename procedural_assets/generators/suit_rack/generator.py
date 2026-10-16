import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SuitRackConfig

class SuitRackGenerator(BaseAssetGenerator[SuitRackConfig]):
    """
    Procedural generator for Suit Rack:
    Heavy steel mobile hanger rack for EVA spacesuits, gloves, and helmets,
    with lower drainage grating and upper helmet mounting horns.
    """

    def generate(self, config: SuitRackConfig = None) -> bpy.types.Object:
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
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")

        # 1. Base floor frame (rectangular tubular sled)
        tube_w = 0.05
        # Side floor skids
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(tube_w, d, tube_w),
                offset=(sx * (w / 2.0 - tube_w / 2.0), 0.0, tube_w / 2.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        # Front and back floor tie bars
        for sy in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(w - 2.0 * tube_w, tube_w, tube_w),
                offset=(0.0, sy * (d / 2.0 - tube_w / 2.0), tube_w / 2.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # 2. Lower boot drainage tray
        if self.config.has_boot_tray:
            MeshBuilder.add_box(
                bm,
                size=(w * 0.88, d * 0.82, 0.02),
                offset=(0.0, 0.0, tube_w + 0.01),
                mat_idx=metal_mat,
                rgba=(0.25, 0.25, 0.28, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("vent_grill")
            )

        # 3. Main vertical upright pillars
        col_h = h - tube_w
        for sx in (-1, 1):
            MeshBuilder.add_box(
                bm,
                size=(tube_w, tube_w * 1.5, col_h),
                offset=(sx * (w / 2.0 - tube_w / 2.0), 0.0, tube_w + col_h / 2.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # 4. Top horizontal hanging beam
        beam_h = 0.06
        beam_z = h - beam_h / 2.0
        MeshBuilder.add_box(
            bm,
            size=(w, tube_w * 1.2, beam_h),
            offset=(0.0, 0.0, beam_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 5. Hanging positions & EVA Suit modules
        num_pos = max(2, min(4, int(self.config.suit_positions)))
        num_occ = max(0, min(num_pos, int(self.config.occupied_suits)))
        spacing = (w - 2.0 * tube_w - 0.2) / float(num_pos)

        for i in range(num_pos):
            pos_x = -(w / 2.0 - tube_w - 0.1) + i * spacing + spacing / 2.0
            
            # Heavy steel hanger triangle hook
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.12,
                segments=6,
                offset=(pos_x, 0.0, beam_z - 0.08),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.7, 0.7, 0.75, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

            # Upper helmet support peg
            if self.config.has_helmet_hooks:
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.012,
                    depth=0.16,
                    segments=6,
                    offset=(pos_x, 0.12, beam_z + 0.05),
                    axis='Y',
                    mat_idx=screen_mat,
                    rgba=(0.95, 0.8, 0.1, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("button_yellow")
                )

            # Hanging Suit silhouette (if occupied)
            if i < num_occ:
                suit_top_z = beam_z - 0.14
                
                # Torso / Upper body EVA pressure suit
                torso_h = 0.65
                torso_w = 0.38
                torso_d = 0.32
                torso_z = suit_top_z - torso_h / 2.0
                MeshBuilder.add_box(
                    bm,
                    size=(torso_w, torso_d, torso_h),
                    offset=(pos_x, 0.0, torso_z),
                    mat_idx=casing_mat,
                    rgba=(0.88, 0.90, 0.92, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                )

                # Chest life support pack (backpack & chest control unit)
                MeshBuilder.add_box(
                    bm,
                    size=(torso_w * 0.75, 0.10, torso_h * 0.55),
                    offset=(pos_x, -torso_d / 2.0 - 0.04, torso_z + 0.05),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

                # Chest telemetry indicator
                MeshBuilder.add_box(
                    bm,
                    size=(0.08, 0.01, 0.08),
                    offset=(pos_x, -torso_d / 2.0 - 0.095, torso_z + 0.12),
                    mat_idx=screen_mat,
                    rgba=(0.85, 0.65, 0.2, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
                )

                # Hanging legs / lower garment
                legs_h = 0.65
                legs_z = torso_z - torso_h / 2.0 - legs_h / 2.0
                for leg_dir in (-1, 1):
                    MeshBuilder.add_box(
                        bm,
                        size=(0.14, 0.20, legs_h),
                        offset=(pos_x + leg_dir * 0.10, 0.0, legs_z),
                        mat_idx=casing_mat,
                        rgba=(0.82, 0.84, 0.86, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                    )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
