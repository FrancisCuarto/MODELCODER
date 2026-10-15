import math
import mathutils
import bmesh
from typing import Optional, List
import random
from ....core.mesh_builder import MeshBuilder

class ControlsComponent:
    """Generates buttons, toggle switches, and rotary dials."""

    @staticmethod
    def add_push_button(
        bm: bmesh.types.BMesh,
        pos: mathutils.Vector,
        size: float,
        color_key: str,
        sides: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Add an industrial push button with bezel rim and colored actuator."""
        bezel_radius = size * 0.6
        bezel_depth = 0.015
        btn_radius = size * 0.45
        btn_depth = 0.025

        # Bezel base (metal or black plastic)
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

        # Button plunger cap
        btn_pos = mathutils.Vector((pos.x, pos.y, pos.z + 0.008))
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=btn_radius,
            depth=btn_depth,
            segments=sides,
            offset=btn_pos,
            axis='Z',
            mat_idx=mat_indices.get(color_key, 0),
            rgba=rgba_map.get(color_key, (0.7, 0.2, 0.2, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

    @staticmethod
    def add_toggle_switch(
        bm: bmesh.types.BMesh,
        pos: mathutils.Vector,
        angle_rad: float,
        sides: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Add an industrial toggle switch with threaded bushing and angled lever."""
        bushing_radius = 0.016
        bushing_depth = 0.012

        # Bushing / nut
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=bushing_radius,
            depth=bushing_depth,
            segments=6,  # hex nut
            offset=pos,
            axis='Z',
            mat_idx=mat_indices.get("screw", 0),
            rgba=rgba_map.get("screw", (0.4, 0.4, 0.4, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

        # Angled toggle lever
        lever_len = 0.04
        lever_radius = 0.006
        # Lever base offset slightly forward
        lever_center = mathutils.Vector((
            pos.x,
            pos.y + math.sin(angle_rad) * (lever_len * 0.4),
            pos.z + math.cos(angle_rad) * (lever_len * 0.4) + 0.008
        ))
        MeshBuilder.add_cylinder(
            bm=bm,
            radius=lever_radius,
            depth=lever_len,
            segments=sides,
            offset=lever_center,
            axis='Y',  # tilt along Y
            mat_idx=mat_indices.get("switch_metal", 0),
            rgba=rgba_map.get("switch_metal", (0.7, 0.7, 0.7, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

    @staticmethod
    def add_rotary_switch(
        bm: bmesh.types.BMesh,
        pos: mathutils.Vector,
        sides: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Add a notched industrial rotary knob."""
        knob_radius = 0.03
        knob_depth = 0.025

        MeshBuilder.add_cylinder(
            bm=bm,
            radius=knob_radius,
            depth=knob_depth,
            segments=max(6, sides),
            offset=pos,
            axis='Z',
            mat_idx=mat_indices.get("switch_base", 0),
            rgba=rgba_map.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
            color_layer=color_layer,
            smooth=False
        )

        # White/metal pointer strip on top of knob
        pointer_offset = mathutils.Vector((pos.x, pos.y + knob_radius * 0.4, pos.z + knob_depth / 2.0 + 0.002))
        MeshBuilder.add_box(
            bm=bm,
            size=mathutils.Vector((0.006, knob_radius * 0.6, 0.004)),
            offset=pointer_offset,
            mat_idx=mat_indices.get("switch_metal", 0),
            rgba=rgba_map.get("switch_metal", (0.8, 0.8, 0.8, 1.0)),
            color_layer=color_layer
        )

    @classmethod
    def build_grid(
        cls,
        bm: bmesh.types.BMesh,
        center: mathutils.Vector,
        width: float,
        height: float,
        rows: int,
        cols: int,
        switch_count: int,
        sides: int,
        rng: random.Random,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        """Build a structured grid of push buttons, toggle switches and knobs."""
        if rows <= 0 or cols <= 0:
            return

        dx = width / max(1, cols)
        dy = height / max(1, rows)
        x_start = center.x - (width / 2.0) + (dx / 2.0)
        y_start = center.y - (height / 2.0) + (dy / 2.0)
        z_pos = center.z

        button_colors = ["button_red", "button_yellow", "button_blue", "button_gray"]

        for r in range(rows):
            for c in range(cols):
                px = x_start + c * dx
                py = y_start + r * dy
                pos = mathutils.Vector((px, py, z_pos))

                choice_val = rng.random()
                if choice_val < 0.65:
                    # Push button
                    btn_color = rng.choice(button_colors)
                    cls.add_push_button(
                        bm=bm,
                        pos=pos,
                        size=min(dx, dy) * 0.4,
                        color_key=btn_color,
                        sides=sides,
                        mat_indices=mat_indices,
                        color_layer=color_layer,
                        rgba_map=rgba_map
                    )
                elif choice_val < 0.85:
                    # Toggle switch
                    angle = rng.choice([-0.35, 0.35])
                    cls.add_toggle_switch(
                        bm=bm,
                        pos=pos,
                        angle_rad=angle,
                        sides=sides,
                        mat_indices=mat_indices,
                        color_layer=color_layer,
                        rgba_map=rgba_map
                    )
                else:
                    # Rotary switch
                    cls.add_rotary_switch(
                        bm=bm,
                        pos=pos,
                        sides=sides,
                        mat_indices=mat_indices,
                        color_layer=color_layer,
                        rgba_map=rgba_map
                    )
