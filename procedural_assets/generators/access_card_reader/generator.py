import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import AccessCardReaderConfig

class AccessCardReaderGenerator(BaseAssetGenerator):
    """
    Procedural generator for wall-mounted security access card readers and numeric keypads.
    Builds beveled security enclosure, magnetic stripe swipe channel, LCD prompt panel,
    status LED bar, and rubberized matrix keypad.
    """

    def generate(self, config: AccessCardReaderConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = AccessCardReaderConfig()

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

        # Status color lookup
        state_colors = {
            "granted": (0.15, 0.95, 0.20, 1.0),
            "denied": (0.95, 0.15, 0.15, 1.0),
            "standby": (0.95, 0.80, 0.15, 1.0),
            "offline": (0.22, 0.22, 0.24, 1.0)
        }
        status_rgba = state_colors.get(self.config.status_state, state_colors["standby"])

        w = 0.16
        h = 0.26
        d = 0.04
        half_w = w * 0.5
        half_h = h * 0.5

        # -------------------------------------------------------------
        # 1. Main Wall Housing
        # -------------------------------------------------------------
        # Back mounting base plate
        MeshBuilder.add_box(
            bm,
            size=(w, 0.015, h),
            offset=(0.0, 0.0075, 0.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
        )
        # Front beveled faceplate
        front_w = w - 0.01
        front_h = h - 0.01
        MeshBuilder.add_box(
            bm,
            size=(front_w, d, front_h),
            offset=(0.0, 0.015 + (d * 0.5), 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        front_y = 0.015 + d

        # -------------------------------------------------------------
        # 2. Magnetic Card Swipe Channel (Right side)
        # -------------------------------------------------------------
        if self.config.reader_style in ("swipe_and_keypad", "rfid_tap"):
            slot_x = half_w - 0.018
            # Guide trench protrusion
            MeshBuilder.add_box(
                bm,
                size=(0.024, 0.02, h * 0.92),
                offset=(slot_x, front_y + 0.01, 0.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Internal dark optical read head slot
            MeshBuilder.add_box(
                bm,
                size=(0.008, 0.015, h * 0.80),
                offset=(slot_x, front_y + 0.018, 0.0),
                mat_idx=metal_mat,
                rgba=(0.08, 0.08, 0.09, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )

        # -------------------------------------------------------------
        # 3. Status Light Bar & LCD Panel (Upper half)
        # -------------------------------------------------------------
        panel_x = -0.015 if self.config.reader_style != "keypad_only" else 0.0

        # Horizontal glowing LED status bar
        MeshBuilder.add_box(
            bm,
            size=(0.09, 0.01, 0.014),
            offset=(panel_x, front_y + 0.005, half_h - 0.035),
            mat_idx=accent_mat,
            rgba=status_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # LCD Prompt Display
        if self.config.has_status_screen:
            # Display bezel frame
            MeshBuilder.add_box(
                bm,
                size=(0.09, 0.008, 0.04),
                offset=(panel_x, front_y + 0.004, half_h - 0.07),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Inner LCD glass
            lcd_rgba = (0.20, 0.45, 0.25, 1.0) if self.config.status_state != "offline" else (0.12, 0.12, 0.14, 1.0)
            MeshBuilder.add_box(
                bm,
                size=(0.078, 0.005, 0.03),
                offset=(panel_x, front_y + 0.008, half_h - 0.07),
                mat_idx=metal_mat,
                rgba=lcd_rgba,
                uv_rect=PS1TextureAtlas.get_rect("computer_screen_crt")
            )

        # -------------------------------------------------------------
        # 4. 3x4 Numeric Keypad Matrix (Lower half)
        # -------------------------------------------------------------
        if self.config.has_keypad:
            # Keypad recess base plate
            MeshBuilder.add_box(
                bm,
                size=(0.088, 0.006, 0.105),
                offset=(panel_x, front_y + 0.003, -0.035),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Button grid: 3 cols x 4 rows
            col_dx = 0.024
            row_dz = 0.022
            btn_w = 0.018
            btn_h = 0.015
            btn_thick = 0.008

            for col in range(3):
                bx = panel_x - col_dx + (col * col_dx)
                for row in range(4):
                    bz = -0.035 + (1.5 * row_dz) - (row * row_dz)
                    MeshBuilder.add_box(
                        bm,
                        size=(btn_w, btn_thick, btn_h),
                        offset=(bx, front_y + 0.006 + (btn_thick * 0.5), bz),
                        mat_idx=casing_mat,
                        rgba=(0.35, 0.35, 0.38, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("control_panel_buttons")
                    )

        # -------------------------------------------------------------
        # 5. Protective Weather Shroud (Optional)
        # -------------------------------------------------------------
        if self.config.weather_shroud:
            shroud_d = 0.08
            # Slanted top roof
            MeshBuilder.add_box(
                bm,
                size=(w + 0.03, shroud_d, 0.015),
                offset=(0.0, (shroud_d * 0.5) - 0.01, half_h + 0.01),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Left & right side cheeks
            for sx in (-(half_w + 0.01), (half_w + 0.01)):
                MeshBuilder.add_box(
                    bm,
                    size=(0.01, shroud_d * 0.7, h + 0.02),
                    offset=(sx, shroud_d * 0.35, 0.0),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                )

        # -------------------------------------------------------------
        # 6. Corner Tamper Screws
        # -------------------------------------------------------------
        screw_inset_x = half_w - 0.014
        screw_inset_z = half_h - 0.014
        for cx in (-screw_inset_x, screw_inset_x):
            for cz in (-screw_inset_z, screw_inset_z):
                MeshBuilder.add_box(
                    bm,
                    size=(0.008, 0.005, 0.008),
                    offset=(cx, front_y + 0.002, cz),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
