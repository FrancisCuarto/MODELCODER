import bpy
import bmesh
import math
from mathutils import Vector
from typing import Dict, Any

from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas
from .config import ReactorControlConsoleConfig

class ReactorControlConsoleGenerator(BaseAssetGenerator):
    """
    Procedural PSX generator for nuclear and thermal reactor master control consoles.
    Features heavy brutalist desk chassis, inclined dial and slider dashboard,
    guarded red emergency SCRAM cutoff button, upper multi-CRT monitoring bridge,
    and annunciator status grid.
    """

    def generate(self, config: ReactorControlConsoleConfig = None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        elif not hasattr(self, "config") or self.config is None:
            self.config = ReactorControlConsoleConfig()

        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        obj, bm = self.create_mesh_object(self.config.name)
        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        w = self.config.console_width
        d = self.config.console_depth
        h = self.config.console_height
        half_w = w * 0.5
        half_d = d * 0.5

        casing_mat = m_idx.get("casing", 0)
        metal_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        accent_mat = m_idx.get("accent", m_idx.get("casing", 0))
        screen_mat = m_idx.get("screen", m_idx.get("casing", 0))

        casing_rgba = self.material_manager.get_rgba("casing")
        metal_rgba = self.material_manager.get_rgba("dark_metal")
        rubber_rgba = (0.15, 0.15, 0.16, 1.0)

        r_state = self.config.reactor_state
        if r_state == "nominal":
            screen_uv = "crt_screen_green"
            screen_rgba = (0.2, 0.85, 0.45, 1.0)
            annunc_uv = "led_green"
        elif r_state == "overload":
            screen_uv = "crt_screen_amber"
            screen_rgba = (0.95, 0.55, 0.15, 1.0)
            annunc_uv = "led_yellow"
        elif r_state == "scram":
            screen_uv = "crt_screen_amber"
            screen_rgba = (0.95, 0.20, 0.15, 1.0)
            annunc_uv = "led_red"
        else: # offline
            screen_uv = "crt_screen_off"
            screen_rgba = (0.2, 0.22, 0.24, 1.0)
            annunc_uv = "metal_dark_grime"

        # -------------------------------------------------------------
        # 1. Base Plinth & Lower Chassis
        # -------------------------------------------------------------
        desk_h = 0.78
        plinth_h = 0.10
        # Floor base plinth
        MeshBuilder.add_box(
            bm,
            size=(w, d, plinth_h),
            offset=(0.0, 0.0, plinth_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Left pedestal cabinet
        ped_w = 0.38
        ped_h = desk_h - plinth_h
        ped_z = plinth_h + ped_h * 0.5
        MeshBuilder.add_box(
            bm,
            size=(ped_w, d - 0.12, ped_h),
            offset=(-half_w + ped_w * 0.5 + 0.05, 0.04, ped_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Right pedestal cabinet
        MeshBuilder.add_box(
            bm,
            size=(ped_w, d - 0.12, ped_h),
            offset=(half_w - ped_w * 0.5 - 0.05, 0.04, ped_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # Kneehole back modesty panel & footrest bar
        MeshBuilder.add_box(
            bm,
            size=(w - ped_w * 2 - 0.10, 0.03, ped_h * 0.75),
            offset=(0.0, half_d - 0.08, plinth_h + ped_h * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Footrest bar
        MeshBuilder.add_cylinder(
            bm,
            radius=0.02,
            depth=w - ped_w * 2 - 0.12,
            segments=6,
            offset=(0.0, 0.0, plinth_h + 0.06),
            axis='X',
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # -------------------------------------------------------------
        # 2. Operator Desk Surface & Padded Armrest
        # -------------------------------------------------------------
        desk_th = 0.05
        MeshBuilder.add_box(
            bm,
            size=(w, d * 0.45, desk_th),
            offset=(0.0, -half_d + (d * 0.45) * 0.5, desk_h - desk_th * 0.5),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_light_brushed")
        )

        # Front padded armrest edge
        MeshBuilder.add_box(
            bm,
            size=(w, 0.06, 0.04),
            offset=(0.0, -half_d + 0.03, desk_h + 0.01),
            mat_idx=metal_mat,
            rgba=rubber_rgba,
            uv_rect=PS1TextureAtlas.get_rect("rubber_black")
        )

        # -------------------------------------------------------------
        # 3. Inclined Dashboard (Switches, Dials & SCRAM Lever)
        # -------------------------------------------------------------
        dash_d = d * 0.28
        dash_h = 0.18
        dash_y = -half_d + d * 0.45 + dash_d * 0.5
        dash_z = desk_h + dash_h * 0.5

        # Wedge dashboard substrate
        MeshBuilder.add_box(
            bm,
            size=(w - 0.06, dash_d, dash_h),
            offset=(0.0, dash_y, dash_z),
            mat_idx=metal_mat,
            rgba=metal_rgba,
            uv_rect=PS1TextureAtlas.get_rect("metal_dark_grime")
        )

        # Analog Dial Gauges
        gauge_count = max(2, min(self.config.dial_gauge_count, 6))
        gauge_spacing = (w * 0.55) / gauge_count
        gauge_start_x = -half_w * 0.40

        for gi in range(gauge_count):
            gx = gauge_start_x + gi * gauge_spacing
            gz = dash_z + 0.04
            MeshBuilder.add_cylinder(
                bm,
                radius=0.038,
                depth=0.02,
                segments=6,
                offset=(gx, dash_y - dash_d * 0.35, gz),
                axis='Y',
                mat_idx=screen_mat,
                rgba=(0.92, 0.92, 0.92, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("gauge_meter")
            )

        # Rocker switches / push button array
        btn_count = 5
        for bi in range(btn_count):
            bx = -half_w * 0.35 + bi * 0.10
            bz = dash_z - 0.05
            b_uv = "button_yellow" if bi % 2 == 0 else "button_white"
            MeshBuilder.add_box(
                bm,
                size=(0.04, 0.02, 0.03),
                offset=(bx, dash_y - dash_d * 0.40, bz),
                mat_idx=metal_mat,
                rgba=(0.9, 0.85, 0.2, 1.0),
                uv_rect=PS1TextureAtlas.get_rect(b_uv)
            )

        # Emergency SCRAM Reactor Trip Button / Lever
        if self.config.has_scram_switch:
            scram_x = half_w * 0.38
            scram_y = dash_y - dash_d * 0.30
            scram_z = dash_z

            # Hazard guard collar
            MeshBuilder.add_box(
                bm,
                size=(0.14, 0.10, 0.04),
                offset=(scram_x, scram_y, scram_z - 0.02),
                mat_idx=accent_mat,
                rgba=(0.95, 0.85, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("hazard_stripes")
            )
            # Big red palm button
            MeshBuilder.add_cylinder(
                bm,
                radius=0.045,
                depth=0.035,
                segments=6,
                offset=(scram_x, scram_y, scram_z + 0.02),
                axis='Z',
                mat_idx=accent_mat,
                rgba=(0.95, 0.15, 0.1, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("button_red")
            )

        # -------------------------------------------------------------
        # 4. Upper CRT Monitoring Bridge & Annunciator Grid
        # -------------------------------------------------------------
        bridge_h = h - (desk_h + dash_h)
        bridge_d = d * 0.26
        bridge_y = half_d - bridge_d * 0.5 - 0.02
        bridge_z = desk_h + dash_h + bridge_h * 0.5

        # Upper bridge chassis
        MeshBuilder.add_box(
            bm,
            size=(w, bridge_d, bridge_h),
            offset=(0.0, bridge_y, bridge_z),
            mat_idx=casing_mat,
            rgba=casing_rgba,
            uv_rect=PS1TextureAtlas.get_rect("painted_metal_white")
        )

        # CRT Monitors
        screen_n = max(2, min(self.config.screen_count, 4))
        screen_w = (w - 0.16) / screen_n
        screen_h = bridge_h * 0.65

        for si in range(screen_n):
            sx = -half_w + 0.08 + si * screen_w + screen_w * 0.5
            sy = bridge_y - bridge_d * 0.5 - 0.005
            sz = bridge_z - bridge_h * 0.10

            # CRT bezel
            MeshBuilder.add_box(
                bm,
                size=(screen_w - 0.04, 0.02, screen_h),
                offset=(sx, sy, sz),
                mat_idx=metal_mat,
                rgba=(0.78, 0.76, 0.72, 1.0),
                uv_rect=PS1TextureAtlas.get_rect("beige_plastic_worn")
            )
            # Phosphor screen face
            MeshBuilder.add_box(
                bm,
                size=(screen_w - 0.08, 0.012, screen_h - 0.04),
                offset=(sx, sy - 0.012, sz),
                mat_idx=screen_mat,
                rgba=screen_rgba,
                uv_rect=PS1TextureAtlas.get_rect(screen_uv)
            )

        # Top Annunciator Status Alarm Bar
        annunc_w = w - 0.10
        annunc_h = 0.06
        annunc_z = h - annunc_h * 0.5 - 0.02
        MeshBuilder.add_box(
            bm,
            size=(annunc_w, 0.02, annunc_h),
            offset=(0.0, bridge_y - bridge_d * 0.5 - 0.01, annunc_z),
            mat_idx=screen_mat,
            rgba=(0.95, 0.90, 0.2, 1.0),
            uv_rect=PS1TextureAtlas.get_rect(annunc_uv)
        )

        self.finalize_mesh(obj, bm)
        self.compact_materials(obj)
        return obj
