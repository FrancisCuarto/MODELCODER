import math
import mathutils
import bmesh
from typing import Optional, List
import random
from ....core.mesh_builder import MeshBuilder

class IndicatorsComponent:
    """Generates status LEDs and round analog telemetry gauges."""

    @staticmethod
    def add_led(
        bm: bmesh.types.BMesh,
        pos: mathutils.Vector,
        color_key: str,
        sides: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Add a faceted low-poly LED with beveled bezel and emissive bulb."""
        bezel_radius = 0.016
        bezel_depth = 0.008
        bulb_radius = 0.010
        bulb_depth = 0.012

        # Bezel ring
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=bezel_radius,
            depth=bezel_depth,
            segments=sides,
            offset=pos,
            axis='Z',
            mat_idx=mat_indices.get("switch_base", 0),
            rgba=rgba_map.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

        # Emissive bulb
        bulb_pos = mathutils.Vector((pos.x, pos.y, pos.z + 0.005))
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=bulb_radius,
            depth=bulb_depth,
            segments=sides,
            offset=bulb_pos,
            axis='Z',
            mat_idx=mat_indices.get(color_key, 0),
            rgba=rgba_map.get(color_key, (0.2, 0.9, 0.2, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

    @staticmethod
    def add_analog_gauge(
        bm: bmesh.types.BMesh,
        pos: mathutils.Vector,
        radius: float,
        sides: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Add a round analog pressure/voltage gauge with pointer needle."""
        gauge_depth = 0.02

        # Outer bezel rim
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=radius,
            depth=gauge_depth,
            segments=sides,
            offset=pos,
            axis='Z',
            mat_idx=mat_indices.get("screw", 0),
            rgba=rgba_map.get("screw", (0.3, 0.3, 0.3, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

        # Gauge dial face plate (flat recessed plate)
        dial_pos = mathutils.Vector((pos.x, pos.y, pos.z + 0.005))
        MeshBuilder.add_circle(
            bm=bm,
            radius=radius * 0.82,
            segments=sides,
            offset=dial_pos,
            axis='Z',
            mat_idx=mat_indices.get("casing_inner", 0),
            rgba=rgba_map.get("casing_inner", (0.8, 0.78, 0.7, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

        # Needle indicator (small thin red wedge pointing at an angle)
        needle_len = radius * 0.65
        angle = math.radians(45.0)
        needle_center = mathutils.Vector((
            pos.x + math.cos(angle) * (needle_len * 0.4),
            pos.y + math.sin(angle) * (needle_len * 0.4),
            pos.z + 0.010
        ))
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((needle_len, 0.004, 0.004)),
            offset=needle_center,
            mat_idx=mat_indices.get("button_red", 0),
            rgba=rgba_map.get("button_red", (0.9, 0.1, 0.1, 1.0)),
            color_layer=color_layer
        )

    @classmethod
    def build_strip(
        cls,
        bm: bmesh.types.BMesh,
        start_pos: mathutils.Vector,
        count: int,
        spacing: float,
        sides: int,
        rng: random.Random,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Build a horizontal strip of status indicator LEDs."""
        led_colors = ["led_green", "led_yellow", "led_red"]
        for i in range(count):
            pos = mathutils.Vector((
                start_pos.x + i * spacing,
                start_pos.y,
                start_pos.z
            ))
            color_choice = rng.choice(led_colors)
            cls.add_led(
                bm=bm,
                pos=pos,
                color_key=color_choice,
                sides=sides,
                mat_indices=mat_indices,
                color_layer=color_layer,
                rgba_map=rgba_map
            )
