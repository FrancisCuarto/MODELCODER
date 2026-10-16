import bpy
import bmesh
import math
from mathutils import Vector, Matrix
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import SecurityCameraConfig

class SecurityCameraGenerator(BaseAssetGenerator):
    """
    Procedural generator for industrial CCTV surveillance cameras.
    Builds wall/ceiling mount plate, articulated extension arm with gimbal knuckle,
    bullet/enclosure or dome camera body, sun shield, optic lens, and recording LED.
    """

    def generate(self, config: SecurityCameraConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = SecurityCameraConfig()

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
        red_rgba = (0.95, 0.10, 0.10, 1.0)
        dark_glass_rgba = (0.08, 0.08, 0.10, 1.0)

        # -------------------------------------------------------------
        # 1. Wall/Ceiling Mounting Plate & Arm
        # -------------------------------------------------------------
        plate_w = 0.11
        plate_h = 0.11
        plate_t = 0.02

        if self.config.mount_type == "ceiling":
            # Flat plate against ceiling at Z=0.0
            MeshBuilder.add_box(
                bm,
                size=(plate_w, plate_w, plate_t),
                offset=(0.0, 0.0, -plate_t * 0.5),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            gimbal_center = Vector((0.0, 0.0, -0.12))
            # Downward drop stem
            MeshBuilder.add_cylinder(
                bm,
                radius=0.018,
                depth=0.10,
                segments=6,
                offset=(0.0, 0.0, -0.06),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
        else:
            # Wall mount against Y=0.0 plane
            MeshBuilder.add_box(
                bm,
                size=(plate_w, plate_t, plate_h),
                offset=(0.0, plate_t * 0.5, 0.0),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
            )
            # Extension arm reaching forward in +Y
            arm_reach = 0.18
            MeshBuilder.add_cylinder(
                bm,
                radius=0.016,
                depth=arm_reach,
                segments=6,
                offset=(0.0, arm_reach * 0.5, 0.0),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            gimbal_center = Vector((0.0, arm_reach, 0.0))

        # Gimbal spherical swivel ball
        MeshBuilder.add_cylinder(
            bm,
            radius=0.028,
            depth=0.05,
            segments=7,
            offset=tuple(gimbal_center),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Camera Body Construction
        # -------------------------------------------------------------
        pan_rad = math.radians(self.config.pan_angle)
        tilt_rad = math.radians(self.config.tilt_angle)
        rot_mat = Matrix.Rotation(pan_rad, 4, 'Z') @ Matrix.Rotation(tilt_rad, 4, 'X')

        cam_faces = []

        if self.config.camera_type == "dome":
            # Hemisphere / octagonal dome casing
            dome_base = MeshBuilder.add_cylinder(
                bm,
                radius=0.08,
                depth=0.03,
                segments=8,
                offset=(0.0, 0.0, -0.015),
                axis='Z',
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            dome_bubble = MeshBuilder.add_cylinder(
                bm,
                radius=0.065,
                depth=0.06,
                segments=8,
                offset=(0.0, 0.0, -0.05),
                axis='Z',
                mat_idx=metal_mat,
                rgba=dark_glass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )
            cam_faces.extend(dome_base)
            cam_faces.extend(dome_bubble)

            if self.config.has_status_led:
                led_face = MeshBuilder.add_cylinder(
                    bm,
                    radius=0.008,
                    depth=0.015,
                    segments=5,
                    offset=(0.04, 0.0, -0.04),
                    axis='Z',
                    mat_idx=accent_mat,
                    rgba=red_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                cam_faces.extend(led_face)
        else:
            # Bullet or Heavy Enclosure camera
            body_l = 0.18
            body_w = 0.075
            body_h = 0.075

            # Main camera chassis box (aligned locally along Y)
            body_box = MeshBuilder.add_box(
                bm,
                size=(body_w, body_l, body_h),
                offset=(0.0, body_l * 0.5 + 0.02, 0.0),
                mat_idx=casing_mat,
                rgba=casing_rgba,
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )
            cam_faces.extend(body_box)

            # Front lens bezel rim
            front_y = body_l + 0.02
            bezel = MeshBuilder.add_cylinder(
                bm,
                radius=0.034,
                depth=0.02,
                segments=7,
                offset=(0.0, front_y + 0.01, 0.0),
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            cam_faces.extend(bezel)

            # Central dark optic lens glass
            glass = MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=0.01,
                segments=7,
                offset=(0.0, front_y + 0.022, 0.0),
                axis='Y',
                mat_idx=metal_mat,
                rgba=dark_glass_rgba,
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )
            cam_faces.extend(glass)

            # Sun shield / weather hood on top
            if self.config.has_sun_shield:
                shield_l = body_l + 0.06
                shield = MeshBuilder.add_box(
                    bm,
                    size=(body_w + 0.02, shield_l, 0.012),
                    offset=(0.0, shield_l * 0.5, (body_h * 0.5) + 0.008),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_plates_rivets")
                )
                cam_faces.extend(shield)

            # Recording status LED
            if self.config.has_status_led:
                led_rgba = red_rgba
                led = MeshBuilder.add_cylinder(
                    bm,
                    radius=0.006,
                    depth=0.012,
                    segments=5,
                    offset=(0.024, front_y + 0.015, 0.024),
                    axis='Y',
                    mat_idx=accent_mat,
                    rgba=led_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
                )
                cam_faces.extend(led)

            # IR LED ring (4 corner indicator studs)
            if self.config.has_ir_ring:
                for ix, iz in ((-0.022, -0.022), (0.022, -0.022), (-0.022, 0.022)):
                    ir_dot = MeshBuilder.add_box(
                        bm,
                        size=(0.007, 0.008, 0.007),
                        offset=(ix, front_y + 0.012, iz),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )
                    cam_faces.extend(ir_dot)

        # Apply Pan/Tilt orientation relative to gimbal center
        cam_verts = list({v for f in cam_faces for v in f.verts})
        trans_mat = Matrix.Translation(gimbal_center)
        bmesh.ops.transform(bm, matrix=trans_mat @ rot_mat, verts=cam_verts)

        # -------------------------------------------------------------
        # 3. Rear Conduit Cable
        # -------------------------------------------------------------
        if self.config.mount_type != "ceiling":
            # Coiled flexible power/signal cord loop
            MeshBuilder.add_cylinder(
                bm,
                radius=0.008,
                depth=arm_reach * 0.8,
                segments=5,
                offset=(0.025, arm_reach * 0.45, -0.035),
                axis='Y',
                mat_idx=metal_mat,
                rgba=(0.12, 0.12, 0.12, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_tread")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
