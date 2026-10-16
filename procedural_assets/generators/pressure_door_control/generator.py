import math
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import PressureDoorControlConfig

class PressureDoorControlGenerator(BaseAssetGenerator[PressureDoorControlConfig]):
    """
    Procedural generator for Pressure Door Control:
    Diegetic bulkhead control panel with bar/psi pressure display, access keypad,
    keycard slot, and status alarm lights.
    """

    def generate(self, config: PressureDoorControlConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        uv_layer = MeshBuilder.get_or_create_uv_layer(bm)
        col_layer = MeshBuilder.get_or_create_color_layer(bm)

        w = self.config.width
        h = self.config.height
        d = self.config.depth

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")

        # 1. Main wall-mount chassis box
        MeshBuilder.add_box(
            bm,
            size=(w, d, h),
            offset=(0.0, d / 2.0, h / 2.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Recessed front face bezel
        face_w = w * 0.90
        face_h = h * 0.92
        face_y = d + 0.005
        MeshBuilder.add_box(
            bm,
            size=(face_w, 0.01, face_h),
            offset=(0.0, face_y, h / 2.0),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 2. Status light lamp at top
        lamp_w = face_w * 0.75
        lamp_h = 0.04
        lamp_z = h * 0.88
        if self.config.status_light == "green":
            led_rect = PS1TextureAtlas.get_rect("led_green")
            led_rgba = (0.1, 0.9, 0.2, 1.0)
        elif self.config.status_light == "red":
            led_rect = PS1TextureAtlas.get_rect("led_red")
            led_rgba = (0.9, 0.1, 0.1, 1.0)
        else:
            led_rect = PS1TextureAtlas.get_rect("led_yellow")
            led_rgba = (0.95, 0.8, 0.1, 1.0)

        MeshBuilder.add_box(
            bm,
            size=(lamp_w, 0.015, lamp_h),
            offset=(0.0, face_y + 0.008, lamp_z),
            mat_idx=screen_mat,
            rgba=led_rgba,
            uv_rect=led_rect
        )

        # 3. Pressure digital readout screen
        screen_w = face_w * 0.82
        screen_h = 0.09
        screen_z = h * 0.72
        disp_rect = PS1TextureAtlas.get_rect("crt_screen_green" if self.config.status_light == "green" else "crt_screen_amber")
        MeshBuilder.add_box(
            bm,
            size=(screen_w, 0.015, screen_h),
            offset=(0.0, face_y + 0.008, screen_z),
            mat_idx=screen_mat,
            rgba=(0.1, 0.8, 0.25, 1.0) if self.config.status_light == "green" else (0.9, 0.6, 0.1, 1.0),
            uv_rect=disp_rect
        )

        # 4. Access keypad
        if self.config.has_keypad:
            keypad_w = face_w * 0.48
            keypad_h = 0.16
            keypad_z = h * 0.44
            keypad_x = -face_w * 0.18
            MeshBuilder.add_box(
                bm,
                size=(keypad_w, 0.015, keypad_h),
                offset=(keypad_x, face_y + 0.008, keypad_z),
                mat_idx=casing_mat,
                rgba=(0.85, 0.85, 0.88, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_white")
            )

        # 5. Keycard reader slot
        if self.config.has_card_slot:
            card_x = face_w * 0.26
            card_z = h * 0.44
            # Reader housing
            MeshBuilder.add_box(
                bm,
                size=(0.045, 0.02, 0.18),
                offset=(card_x, face_y + 0.01, card_z),
                mat_idx=metal_mat,
                rgba=(0.15, 0.15, 0.18, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Slot groove
            MeshBuilder.add_box(
                bm,
                size=(0.008, 0.01, 0.14),
                offset=(card_x, face_y + 0.021, card_z),
                mat_idx=metal_mat,
                rgba=(0.05, 0.05, 0.05, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        # 6. Emergency vent button
        if self.config.has_emergency_vent_button:
            vent_z = h * 0.18
            # Guard collar
            MeshBuilder.add_cylinder(
                bm,
                radius=0.038,
                depth=0.02,
                segments=8,
                offset=(0.0, face_y + 0.01, vent_z),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.9, 0.8, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            # Red push button
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=0.025,
                segments=8,
                offset=(0.0, face_y + 0.018, vent_z),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.9, 0.15, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        # 7. Bottom electrical conduit fitting
        MeshBuilder.add_cylinder(
            bm,
            radius=0.018,
            depth=0.06,
            segments=6,
            offset=(0.0, d * 0.5, -0.03),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
