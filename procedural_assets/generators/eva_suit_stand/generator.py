import math
import mathutils
import bpy
import bmesh
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import EvaSuitStandConfig

class EvaSuitStandGenerator(BaseAssetGenerator[EvaSuitStandConfig]):
    """
    Procedural generator for EVA Suit Stand:
    Standalone maintenance and inspection rig with telescoping central pylon,
    articulated telemetry screen, and full pressurized EVA suit mannequin.
    """

    def generate(self, config: EvaSuitStandConfig = None) -> bpy.types.Object:
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

        h = self.config.height
        bw = self.config.base_width

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        brass_mat = m_idx.get("brass", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        brass_rgba = (0.85, 0.68, 0.22, 1.0)

        # 1. Heavy cross-shaped base plate
        base_h = 0.06
        for ang in (0.0, math.pi / 2.0):
            MeshBuilder.add_box(
                bm,
                size=(bw, 0.16, base_h),
                offset=(0.0, 0.0, base_h / 2.0),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

        # Central base collar
        MeshBuilder.add_cylinder(
            bm,
            radius=0.12,
            depth=0.12,
            segments=8,
            offset=(0.0, 0.0, base_h + 0.06),
            axis='Z',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # 2. Central vertical support column (telescoping steel pylon)
        col_h = h * 0.88
        MeshBuilder.add_cylinder(
            bm,
            radius=0.045,
            depth=col_h,
            segments=6,
            offset=(0.0, -0.05, col_h / 2.0 + base_h),
            axis='Z',
            mat_idx=metal_mat,
            rgba=(0.7, 0.72, 0.75, 1.0),
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # 3. Shoulder yoke crossbar
        yoke_z = h * 0.78
        yoke_w = 0.52
        MeshBuilder.add_box(
            bm,
            size=(yoke_w, 0.10, 0.05),
            offset=(0.0, -0.05, yoke_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Neck mounting collar ring
        MeshBuilder.add_cylinder(
            bm,
            radius=0.14,
            depth=0.06,
            segments=8,
            offset=(0.0, 0.0, yoke_z + 0.08),
            axis='Z',
            mat_idx=brass_mat,
            rgba=brass_rgba,
            uv_rect=PS1TextureAtlas.get_rect("cartridge_amber")
        )

        # 4. Mounted EVA Suit (if present)
        if self.config.has_suit_mounted:
            torso_h = 0.65
            torso_w = 0.44
            torso_d = 0.34
            torso_z = yoke_z - torso_h / 2.0 + 0.02

            # Main torso body
            MeshBuilder.add_box(
                bm,
                size=(torso_w, torso_d, torso_h),
                offset=(0.0, 0.0, torso_z),
                mat_idx=casing_mat,
                rgba=(0.90, 0.92, 0.94, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
            )

            # Chest telemetry & valve box
            MeshBuilder.add_box(
                bm,
                size=(0.20, 0.08, 0.22),
                offset=(0.0, torso_d / 2.0 + 0.04, torso_z + 0.05),
                mat_idx=metal_mat,
                rgba=(0.2, 0.22, 0.25, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )
            # Chest status dial
            MeshBuilder.add_cylinder(
                bm,
                radius=0.035,
                depth=0.015,
                segments=6,
                offset=(0.0, torso_d / 2.0 + 0.085, torso_z + 0.05),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.95, 0.95, 0.95, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

            # Back Primary Life Support System (PLSS backpack)
            plss_w = torso_w * 0.85
            plss_h = torso_h * 0.90
            plss_d = 0.18
            MeshBuilder.add_box(
                bm,
                size=(plss_w, plss_d, plss_h),
                offset=(0.0, -torso_d / 2.0 - plss_d / 2.0 - 0.02, torso_z),
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
            )

            # Dual O2 tanks on backpack
            for sx in (-0.10, 0.10):
                MeshBuilder.add_cylinder(
                    bm,
                    radius=0.045,
                    depth=plss_h * 0.8,
                    segments=6,
                    offset=(sx, -torso_d / 2.0 - plss_d - 0.04, torso_z),
                    axis='Z',
                    mat_idx=screen_mat,
                    rgba=(0.2, 0.75, 0.85, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("oxygen_cyan_glow")
                )

            # Arms
            arm_len = 0.55
            arm_r = 0.065
            pose = self.config.arm_pose
            for sx in (-1, 1):
                sh_x = sx * (torso_w / 2.0 + arm_r)
                if pose == "t_pose":
                    # Arms extended horizontal
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=arm_r,
                        depth=arm_len,
                        segments=6,
                        offset=(sx * (torso_w / 2.0 + arm_len / 2.0), 0.0, yoke_z - 0.05),
                        axis='X',
                        mat_idx=casing_mat,
                        rgba=(0.88, 0.9, 0.92, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                    )
                elif pose == "extended":
                    # Arms angled 45 forward
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=arm_r,
                        depth=arm_len,
                        segments=6,
                        offset=(sh_x, arm_len * 0.35, yoke_z - arm_len * 0.35),
                        axis='Z',
                        mat_idx=casing_mat,
                        rgba=(0.88, 0.9, 0.92, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                    )
                else:
                    # Relaxed hanging vertically
                    MeshBuilder.add_cylinder(
                        bm,
                        radius=arm_r,
                        depth=arm_len,
                        segments=6,
                        offset=(sh_x, 0.0, yoke_z - arm_len / 2.0 - 0.05),
                        axis='Z',
                        mat_idx=casing_mat,
                        rgba=(0.88, 0.9, 0.92, 1.0),
                        uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
                    )

            # Legs and Boots clamped to base
            leg_h = torso_z - torso_h / 2.0 - base_h
            for sx in (-0.12, 0.12):
                MeshBuilder.add_box(
                    bm,
                    size=(0.16, 0.22, leg_h),
                    offset=(sx, 0.0, base_h + leg_h / 2.0),
                    mat_idx=casing_mat,
                    rgba=(0.85, 0.87, 0.90, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("rubber_black")
                )
                # Boot foot clamp
                MeshBuilder.add_box(
                    bm,
                    size=(0.18, 0.28, 0.10),
                    offset=(sx, 0.04, base_h + 0.05),
                    mat_idx=metal_mat,
                    rgba=(0.12, 0.12, 0.14, 1.0),
                    uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
                )

        # 5. Diagnostic terminal tablet mounted on articulated arm
        if self.config.has_diagnostic_tablet:
            arm_x = bw * 0.40
            arm_z = h * 0.55
            # Articulated arm tube
            MeshBuilder.add_cylinder(
                bm,
                radius=0.015,
                depth=0.35,
                segments=4,
                offset=(arm_x * 0.6, 0.15, arm_z),
                axis='X',
                mat_idx=metal_mat,
                rgba=metal_rgba,
                uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
            )
            # Tablet screen box
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.24, 0.18),
                offset=(arm_x, 0.22, arm_z + 0.05),
                mat_idx=casing_mat,
                rgba=(0.8, 0.8, 0.82, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )
            # Screen face
            MeshBuilder.add_box(
                bm,
                size=(0.005, 0.20, 0.14),
                offset=(arm_x - 0.021, 0.22, arm_z + 0.05),
                mat_idx=screen_mat,
                rgba=(0.1, 0.85, 0.3, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("crt_screen_green")
            )

        # 6. Service umbilical conduit snaking to floor
        if self.config.has_service_umbilical:
            umb_x = -bw * 0.30
            MeshBuilder.add_cylinder(
                bm,
                radius=0.025,
                depth=h * 0.65,
                segments=6,
                offset=(umb_x, -0.15, (h * 0.65) / 2.0 + base_h),
                axis='Z',
                mat_idx=metal_mat,
                rgba=(0.08, 0.08, 0.08, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("rubber_black")
            )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
