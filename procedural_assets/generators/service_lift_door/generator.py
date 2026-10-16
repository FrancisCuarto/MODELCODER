import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ServiceLiftDoorConfig

class ServiceLiftDoorGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for heavy industrial freight elevator / service lift doors.
    Builds structural channel jambs, overhead counterweight cable housings, bi-parting door leaves,
    forklift impact kickplates, hall call stations, and SWL load capacity plaques.
    """

    def generate(self, config: ServiceLiftDoorConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = ServiceLiftDoorConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.door_width
        h = self.config.door_height
        d = self.config.frame_depth
        half_w = w * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        kickplate_rgba = (0.35, 0.36, 0.38, 1.0)
        hazard_rgba = (0.95, 0.85, 0.20, 1.0)

        # -------------------------------------------------------------
        # 1. Structural Frame Portal (Jambs and Lintel Header)
        # -------------------------------------------------------------
        jamb_w = 0.16
        lintel_h = 0.28
        # Left column jamb
        MeshBuilder.add_box(
            bm,
            size=(jamb_w, d, h + lintel_h),
            offset=(-half_w - jamb_w * 0.5, d * 0.5, (h + lintel_h) * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Right column jamb
        MeshBuilder.add_box(
            bm,
            size=(jamb_w, d, h + lintel_h),
            offset=(half_w + jamb_w * 0.5, d * 0.5, (h + lintel_h) * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Heavy overhead lintel header beam
        MeshBuilder.add_box(
            bm,
            size=(w + jamb_w * 2, d * 1.10, lintel_h),
            offset=(0.0, d * 0.5, h + lintel_h * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Hazard stripe band across the lintel soffit
        MeshBuilder.add_box(
            bm,
            size=(w, 0.02, 0.08),
            offset=(0.0, d * 0.5 + 0.05, h + 0.04),
            mat_idx=accent_mat,
            rgba=hazard_rgba,
            uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
        )

        # Floor threshold guide track
        MeshBuilder.add_box(
            bm,
            size=(w, d * 0.70, 0.03),
            offset=(0.0, d * 0.5, 0.015),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Dark lift shaft interior void
        MeshBuilder.add_box(
            bm,
            size=(w, 0.02, h),
            offset=(0.0, 0.01, h * 0.5),
            mat_idx=metal_mat,
            rgba=(0.05, 0.06, 0.07, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Bi-Parting Telescoping Door Leaves
        # -------------------------------------------------------------
        leaf_w = w * 0.51
        leaf_th = 0.045
        leaf_h = h * 0.98

        state = self.config.door_state
        if state == "closed" or state == "maintenance_locked":
            offset_left = -leaf_w * 0.5
            offset_right = leaf_w * 0.5
        elif state == "open_partial":
            offset_left = -leaf_w * 0.5 - w * 0.35
            offset_right = leaf_w * 0.5 + w * 0.35
        elif state == "jammed_open":
            offset_left = -leaf_w * 0.5 - w * 0.20
            offset_right = leaf_w * 0.5 + w * 0.12
        else:
            offset_left = -leaf_w * 0.5
            offset_right = leaf_w * 0.5

        door_y = d * 0.5

        # Left Door Leaf
        MeshBuilder.add_box(
            bm,
            size=(leaf_w, leaf_th, leaf_h),
            offset=(offset_left, door_y, leaf_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        # Right Door Leaf
        MeshBuilder.add_box(
            bm,
            size=(leaf_w, leaf_th, leaf_h),
            offset=(offset_right, door_y + 0.015, leaf_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Lower anti-impact kickplates on both leaves
        if self.config.has_toe_guard_kickplate:
            kick_h = 0.55
            # Left kickplate
            MeshBuilder.add_box(
                bm,
                size=(leaf_w * 0.96, 0.015, kick_h),
                offset=(offset_left, door_y + leaf_th * 0.5 + 0.008, kick_h * 0.5 + 0.04),
                mat_idx=metal_mat,
                rgba=kickplate_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Right kickplate
            MeshBuilder.add_box(
                bm,
                size=(leaf_w * 0.96, 0.015, kick_h),
                offset=(offset_right, door_y + leaf_th * 0.5 + 0.023, kick_h * 0.5 + 0.04),
                mat_idx=metal_mat,
                rgba=kickplate_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # Upper vision panel slits
        slit_h = 0.40
        slit_w = 0.12
        slit_z = h * 0.65
        # Left vision panel
        MeshBuilder.add_box(
            bm,
            size=(slit_w, leaf_th * 1.2, slit_h),
            offset=(offset_left + leaf_w * 0.2, door_y, slit_z),
            mat_idx=accent_mat,
            rgba=(0.3, 0.55, 0.65, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
        )
        # Right vision panel
        MeshBuilder.add_box(
            bm,
            size=(slit_w, leaf_th * 1.2, slit_h),
            offset=(offset_right - leaf_w * 0.2, door_y + 0.015, slit_z),
            mat_idx=accent_mat,
            rgba=(0.3, 0.55, 0.65, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
        )

        # Maintenance Lockout Bar (if locked)
        if state == "maintenance_locked":
            MeshBuilder.add_box(
                bm,
                size=(w * 0.85, 0.03, 0.08),
                offset=(0.0, door_y + leaf_th + 0.03, h * 0.5),
                mat_idx=accent_mat,
                rgba=hazard_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )

        # -------------------------------------------------------------
        # 3. Wall Hall Call Station & Floor Display
        # -------------------------------------------------------------
        if self.config.has_call_station:
            call_x = half_w + jamb_w + 0.12
            call_y = d * 0.45
            call_z = 1.35
            # Call box enclosure
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.08, 0.32),
                offset=(call_x, call_y, call_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Digital floor LED segment
            MeshBuilder.add_box(
                bm,
                size=(0.08, 0.015, 0.06),
                offset=(call_x, call_y + 0.045, call_z + 0.09),
                mat_idx=screen_mat,
                rgba=(0.95, 0.65, 0.15, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_amber")
            )
            # Call call button (illuminated halo)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.022,
                depth=0.02,
                segments=6,
                offset=(call_x, call_y + 0.045, call_z - 0.02),
                axis='Y',
                mat_idx=accent_mat,
                rgba=(0.95, 0.85, 0.20, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_yellow")
            )
            # Key switch slot
            MeshBuilder.add_box(
                bm,
                size=(0.03, 0.01, 0.03),
                offset=(call_x, call_y + 0.045, call_z - 0.09),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("switch_metal")
            )

        # -------------------------------------------------------------
        # 4. SWL Capacity Warning Sign
        # -------------------------------------------------------------
        if self.config.has_capacity_sign:
            sign_z = h + lintel_h * 0.5
            MeshBuilder.add_box(
                bm,
                size=(0.65, 0.015, 0.14),
                offset=(0.0, d + 0.01, sign_z),
                mat_idx=accent_mat,
                rgba=hazard_rgba,
                uv_rect=PS1TextureAtlas.get_rect("caution_label")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
