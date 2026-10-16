import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import MaintenanceHatchConfig

class MaintenanceHatchGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for pressure-tight utility maintenance hatches.
    Builds bulkhead coaming frames, hinged access leaves with rotation angles,
    central handwheel or perimeter dogging latches, viewports, and interlock beacons.
    """

    def generate(self, config: MaintenanceHatchConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = MaintenanceHatchConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.width
        h = self.config.height
        d = self.config.hatch_depth
        half_w = w * 0.5
        half_h = h * 0.5

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        rubber_rgba = (0.12, 0.12, 0.14, 1.0)
        wheel_rgba = (0.85, 0.40, 0.15, 1.0)

        # -------------------------------------------------------------
        # 1. Bulkhead Perimeter Coaming Frame
        # -------------------------------------------------------------
        flange_th = 0.035
        coaming_w = 0.06
        # Top frame
        MeshBuilder.add_box(
            bm,
            size=(w + coaming_w * 2, d * 0.5, coaming_w),
            offset=(0.0, d * 0.25, half_h + coaming_w * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Bottom frame
        MeshBuilder.add_box(
            bm,
            size=(w + coaming_w * 2, d * 0.5, coaming_w),
            offset=(0.0, d * 0.25, -half_h - coaming_w * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Left frame
        MeshBuilder.add_box(
            bm,
            size=(coaming_w, d * 0.5, h),
            offset=(-half_w - coaming_w * 0.5, d * 0.25, 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )
        # Right frame
        MeshBuilder.add_box(
            bm,
            size=(coaming_w, d * 0.5, h),
            offset=(half_w + coaming_w * 0.5, d * 0.25, 0.0),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Dark interior cavity backing (utility void)
        MeshBuilder.add_box(
            bm,
            size=(w - 0.02, 0.01, h - 0.02),
            offset=(0.0, 0.01, 0.0),
            mat_idx=metal_mat,
            rgba=(0.06, 0.07, 0.08, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 2. Heavy Bulkhead Strap Hinges (Left side)
        # -------------------------------------------------------------
        hinge_x = -half_w - coaming_w * 0.2
        hinge_y = d * 0.5
        for hz in (-half_h * 0.65, half_h * 0.65):
            MeshBuilder.add_box(
                bm,
                size=(0.045, 0.06, 0.08),
                offset=(hinge_x, hinge_y, hz),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Hinge pin
            MeshBuilder.add_cylinder(
                bm,
                radius=0.014,
                depth=0.10,
                segments=5,
                offset=(hinge_x, hinge_y, hz),
                axis='Z',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        # -------------------------------------------------------------
        # 3. Rotating Hatch Leaf
        # -------------------------------------------------------------
        angle_rad = math.radians(self.config.open_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        def rotate_point(lx, ly, lz):
            # Rotate around (hinge_x, hinge_y) in XY plane
            dx = lx - hinge_x
            dy = ly - hinge_y
            rx = hinge_x + dx * cos_a - dy * sin_a
            ry = hinge_y + dx * sin_a + dy * cos_a
            return (rx, ry, lz)

        # Main hatch door slab
        door_th = 0.045
        door_w = w * 0.96
        door_h = h * 0.96

        p_door = rotate_point(0.0, d * 0.5 + door_th * 0.5, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(door_w, door_th, door_h),
            offset=p_door,
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Neoprene sealing gasket lip
        p_seal = rotate_point(0.0, d * 0.5 - 0.005, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(door_w * 0.98, 0.012, door_h * 0.98),
            offset=p_seal,
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # Diagonal cross-stiffening rib on the face of the hatch
        p_rib1 = rotate_point(0.0, d * 0.5 + door_th + 0.01, 0.0)
        MeshBuilder.add_box(
            bm,
            size=(door_w * 0.85, 0.018, 0.035),
            offset=p_rib1,
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )
        MeshBuilder.add_box(
            bm,
            size=(0.035, 0.018, door_h * 0.85),
            offset=p_rib1,
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # -------------------------------------------------------------
        # 4. Dogging Latch Mechanism
        # -------------------------------------------------------------
        mech = self.config.dogging_mechanism
        mech_y = d * 0.5 + door_th + 0.02

        if mech == "central_wheel":
            # Handwheel center hub
            p_hub = rotate_point(0.0, mech_y + 0.02, 0.0)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.045,
                depth=0.04,
                segments=6,
                offset=p_hub,
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Handwheel outer ring
            p_ring = rotate_point(0.0, mech_y + 0.04, 0.0)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.14,
                depth=0.02,
                segments=8,
                offset=p_ring,
                axis='Y',
                mat_idx=accent_mat,
                rgba=wheel_rgba,
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            # Wheel spokes (horizontal & vertical bars)
            MeshBuilder.add_box(
                bm,
                size=(0.26, 0.016, 0.02),
                offset=p_ring,
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            MeshBuilder.add_box(
                bm,
                size=(0.02, 0.016, 0.26),
                offset=p_ring,
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )

        elif mech == "perimeter_latches":
            # 4 rotating dog-clamps on corners
            for cx in (-door_w * 0.35, door_w * 0.35):
                for cz in (-door_h * 0.35, door_h * 0.35):
                    p_latch = rotate_point(cx, mech_y + 0.015, cz)
                    MeshBuilder.add_box(
                        bm,
                        size=(0.06, 0.025, 0.035),
                        offset=p_latch,
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                    )

        else: # quick_release lever
            p_lever = rotate_point(0.0, mech_y + 0.02, 0.0)
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.04, 0.05),
                offset=p_lever,
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Heavy throw arm
            MeshBuilder.add_box(
                bm,
                size=(0.025, 0.02, 0.28),
                offset=rotate_point(0.0, mech_y + 0.04, 0.08),
                mat_idx=accent_mat,
                rgba=(0.90, 0.15, 0.12, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        # -------------------------------------------------------------
        # 5. Reinforced Viewport (Optional)
        # -------------------------------------------------------------
        if self.config.has_viewport:
            p_vp = rotate_point(0.0, d * 0.5 + door_th * 0.5, door_h * 0.25)
            # Steel peephole rim
            MeshBuilder.add_cylinder(
                bm,
                radius=0.09,
                depth=door_th * 1.3,
                segments=6,
                offset=p_vp,
                axis='Y',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Glass center
            MeshBuilder.add_cylinder(
                bm,
                radius=0.065,
                depth=door_th * 1.35,
                segments=6,
                offset=p_vp,
                axis='Y',
                mat_idx=accent_mat,
                rgba=(0.3, 0.65, 0.75, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("glass_reinforced")
            )

        # -------------------------------------------------------------
        # 6. Overhead Interlock / Pressure Status Light (Optional)
        # -------------------------------------------------------------
        if self.config.has_interlock_light:
            light_z = half_h + coaming_w + 0.06
            # Mount box
            MeshBuilder.add_box(
                bm,
                size=(0.10, 0.05, 0.06),
                offset=(0.0, d * 0.35, light_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Indicator lens (Green = pressurized/nominal, Red = open/alarm)
            is_closed = (self.config.open_angle <= 5.0)
            lens_uv = "led_green" if is_closed else "led_red"
            lens_rgba = (0.2, 0.9, 0.3, 1.0) if is_closed else (0.95, 0.15, 0.1, 1.0)

            MeshBuilder.add_box(
                bm,
                size=(0.06, 0.02, 0.035),
                offset=(0.0, d * 0.35 + 0.03, light_z),
                mat_idx=accent_mat,
                rgba=lens_rgba,
                uv_rect=PS1TextureAtlas.get_rect(lens_uv)
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
