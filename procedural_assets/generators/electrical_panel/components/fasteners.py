import mathutils
import bmesh
from typing import Optional, List
from ....core.mesh_builder import MeshBuilder

class FastenersComponent:
    """Generates industrial mounting screws and corner bolts."""

    @staticmethod
    def build(
        bm: bmesh.types.BMesh,
        width: float,
        height: float,
        depth: float,
        margin: float,
        sides: int,
        add_side_bolts: bool,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        bolt_radius = min(width, height) * 0.025
        bolt_depth = 0.012
        front_z = depth + (bolt_depth / 2.0)

        # 4 corners
        x_span = (width / 2.0) - margin
        y_span = (height / 2.0) - margin

        corners = [
            mathutils.Vector((-x_span, y_span, front_z)),
            mathutils.Vector((x_span, y_span, front_z)),
            mathutils.Vector((-x_span, -y_span, front_z)),
            mathutils.Vector((x_span, -y_span, front_z)),
        ]

        # If panel is tall enough and budget allows, add 2 middle side bolts
        if add_side_bolts and height > 0.8:
            corners.append(mathutils.Vector((-x_span, 0.0, front_z)))
            corners.append(mathutils.Vector((x_span, 0.0, front_z)))

        for pos in corners:
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=bolt_radius,
                depth=bolt_depth,
                segments=sides,
                offset=pos,
                axis='Z',
                mat_idx=mat_indices.get("screw", 0),
                rgba=rgba_map.get("screw", (0.3, 0.3, 0.3, 1.0)),
                color_layer=color_layer,
                smooth=False
            )
