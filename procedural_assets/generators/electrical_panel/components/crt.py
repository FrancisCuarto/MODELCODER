import mathutils
import bmesh
from typing import Optional
from ....core.mesh_builder import MeshBuilder

class CRTComponent:
    """Generates retrofuturistic CRT display unit with convex glass bulge and frame."""

    @staticmethod
    def build(
        bm: bmesh.types.BMesh,
        screen_w: float,
        screen_h: float,
        bulge: float,
        center_pos: mathutils.Vector,
        phosphor_color: str,  # "green" or "amber"
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        screen_mat_key = "crt_screen_green" if phosphor_color == "green" else "crt_screen_amber"

        # 1. Screen bezel and bulging glass lattice
        MeshBuilder.add_crt_screen(
            bm=bm,
            width=screen_w,
            height=screen_h,
            bulge=bulge,
            offset=center_pos,
            screen_mat_idx=mat_indices.get(screen_mat_key, 0),
            screen_rgba=rgba_map.get(screen_mat_key, (0.1, 0.9, 0.3, 1.0)),
            frame_mat_idx=mat_indices.get("crt_frame", 0),
            frame_rgba=rgba_map.get("crt_frame", (0.1, 0.1, 0.1, 1.0)),
            color_layer=color_layer
        )

        # 2. CRT power indicator LED / brightness dial beside the monitor
        led_offset = mathutils.Vector((
            center_pos.x + (screen_w / 2.0) + 0.035,
            center_pos.y - (screen_h / 2.0) + 0.02,
            center_pos.z + 0.025
        ))
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=0.012,
            depth=0.015,
            segments=4,
            offset=led_offset,
            axis='Z',
            mat_idx=mat_indices.get("led_green", 0),
            rgba=rgba_map.get("led_green", (0.1, 0.9, 0.2, 1.0)),
            color_layer=color_layer,
            smooth=False
        )
