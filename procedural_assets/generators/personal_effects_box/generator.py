import math
import mathutils
from mathutils import Vector, Matrix
import bpy
import bmesh
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import PersonalEffectsBoxConfig

class PersonalEffectsBoxGenerator(BaseAssetGenerator[PersonalEffectsBoxConfig]):
    """
    Procedural generator for hermetic crew personal effects trunks.
    Constructs reinforced molded casing, corner impact bumpers, rear hinges,
    dual front draw latches, folding bail handle, stencil crew ID plate,
    and open/closed lid states with interior compartment items.
    """

    def generate(self, config: PersonalEffectsBoxConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = PersonalEffectsBoxConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        casing_mat = m_idx.get("casing", 0)
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))

        metal_rgba = self.material_manager.get_rgba("dark_metal")
        casing_rgba = self.material_manager.get_rgba("casing")
        accent_rgba = self.material_manager.get_rgba("accent")

        w = self.config.width
        d = self.config.depth
        h = self.config.height

        hb = h * 0.70  # Base container height
        hl = h * 0.30  # Lid height

        # -------------------------------------------------------------
        # 1. Base Container Tub
        # -------------------------------------------------------------
        MeshBuilder.add_box(
            bm,
            size=(w, d, hb),
            offset=(0.0, 0.0, hb * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Base stiffening ribbing (horizontal band near perimeter)
        MeshBuilder.add_box(
            bm,
            size=(w * 1.02, d * 1.02, 0.02),
            offset=(0.0, 0.0, hb * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # -------------------------------------------------------------
        # 2. Corner Impact Bumpers (4 vertical corner gussets)
        # -------------------------------------------------------------
        if self.config.has_corner_gussets:
            bw = 0.035
            bd = 0.035
            bh = hb * 0.90
            for sx in (-1.0, 1.0):
                for sy in (-1.0, 1.0):
                    cx = sx * (w * 0.5 - bw * 0.4)
                    cy = sy * (d * 0.5 - bd * 0.4)
                    MeshBuilder.add_box(
                        bm,
                        size=(bw, bd, bh),
                        offset=(cx, cy, bh * 0.5),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        # -------------------------------------------------------------
        # 3. Rear Hinges (2 hinge barrels)
        # -------------------------------------------------------------
        hinge_y = d * 0.5 + 0.008
        hinge_z = hb
        for sx in (-1.0, 1.0):
            hx = sx * (w * 0.28)
            MeshBuilder.add_cylinder(
                bm,
                radius=0.010,
                depth=0.04,
                segments=6,
                offset=(hx, hinge_y, hinge_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 4. Front Latches (2 draw latches)
        # -------------------------------------------------------------
        if self.config.has_latches:
            latch_y = -d * 0.5 - 0.008
            for sx in (-1.0, 1.0):
                lx = sx * (w * 0.25)
                # Lower catch plate on base
                MeshBuilder.add_box(
                    bm,
                    size=(0.024, 0.012, 0.035),
                    offset=(lx, latch_y, hb - 0.02),
                    mat_idx=metal_mat,
                    rgba=(0.7, 0.72, 0.75, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
                )
                # Upper latch clasp
                clasp_z = hb + 0.01 if self.config.box_state != "open" else hb - 0.005
                MeshBuilder.add_box(
                    bm,
                    size=(0.018, 0.014, 0.022),
                    offset=(lx, latch_y, clasp_z),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # -------------------------------------------------------------
        # 5. Front Folding Bail Handle
        # -------------------------------------------------------------
        if self.config.has_handle:
            hy = -d * 0.5 - 0.012
            hz = hb * 0.5
            handle_w = 0.12
            # Handle side brackets
            for sx in (-1.0, 1.0):
                MeshBuilder.add_box(
                    bm,
                    size=(0.018, 0.020, 0.025),
                    offset=(sx * (handle_w * 0.5), hy, hz),
                    mat_idx=metal_mat,
                    rgba=metal_rgba,
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )
            # Grip crossbar
            MeshBuilder.add_cylinder(
                bm,
                radius=0.009,
                depth=handle_w,
                segments=6,
                offset=(0.0, hy - 0.014, hz),
                axis='X',
                mat_idx=metal_mat,
                rgba=(0.3, 0.3, 0.35, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # -------------------------------------------------------------
        # 6. Crew Stencil ID Nameplate
        # -------------------------------------------------------------
        if self.config.has_nameplate:
            plate_w = min(0.18, w * 0.45)
            plate_h = 0.045
            MeshBuilder.add_box(
                bm,
                size=(plate_w, 0.004, plate_h),
                offset=(0.0, -d * 0.5 - 0.002, hb * 0.45),
                mat_idx=screen_mat,
                rgba=(0.85, 0.88, 0.85, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("caution_label")
            )

        # -------------------------------------------------------------
        # 7. Lid Assembly (Closed vs Open)
        # -------------------------------------------------------------
        lid_w = w * 1.01
        lid_d = d * 1.01

        # Track vertices of the lid so we can rotate if open
        lid_verts_before = set(bm.verts)

        # Build lid in closed position first
        MeshBuilder.add_box(
            bm,
            size=(lid_w, lid_d, hl),
            offset=(0.0, 0.0, hb + hl * 0.5),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Lid top recess / bevel rim
        MeshBuilder.add_box(
            bm,
            size=(lid_w * 0.88, lid_d * 0.86, 0.015),
            offset=(0.0, 0.0, hb + hl + 0.005),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Top corner bumpers on lid
        if self.config.has_corner_gussets:
            for sx in (-1.0, 1.0):
                for sy in (-1.0, 1.0):
                    cx = sx * (w * 0.5 - 0.035 * 0.4)
                    cy = sy * (d * 0.5 - 0.035 * 0.4)
                    MeshBuilder.add_box(
                        bm,
                        size=(0.035, 0.035, hl * 0.8),
                        offset=(cx, cy, hb + hl * 0.5),
                        mat_idx=metal_mat,
                        rgba=metal_rgba,
                        uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                    )

        lid_verts_new = [v for v in bm.verts if v not in lid_verts_before]

        if self.config.box_state == "open":
            # Rotate lid open around rear hinge axis
            pivot = Vector((0.0, d * 0.5, hb))
            rot_mat = Matrix.Rotation(math.radians(-80.0), 3, 'X')
            for v in lid_verts_new:
                rel = v.co - pivot
                v.co = pivot + (rot_mat @ rel)

            # Inside cavity item: small personal datapad / journal
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.09, 0.02),
                offset=(0.05, 0.02, hb * 0.85),
                mat_idx=metal_mat,
                rgba=(0.2, 0.22, 0.25, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Datapad screen
            MeshBuilder.add_box(
                bm,
                size=(0.10, 0.065, 0.004),
                offset=(0.05, 0.02, hb * 0.85 + 0.011),
                mat_idx=screen_mat,
                rgba=(0.18, 0.45, 0.55, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )
        elif self.config.box_state == "damaged":
            # Slightly misaligned / dented lid
            pivot = Vector((0.0, d * 0.5, hb))
            rot_mat = Matrix.Rotation(math.radians(-6.0), 3, 'X')
            for v in lid_verts_new:
                rel = v.co - pivot
                v.co = pivot + (rot_mat @ rel)

        self.finalize_mesh(obj, bm)
        return obj
