import mathutils
import bmesh
from typing import Optional, List
from ....core.mesh_builder import MeshBuilder

class CasingComponent:
    """Generates industrial electrical panel enclosure with mounting flanges and vents."""

    @staticmethod
    def build(
        bm: bmesh.types.BMesh,
        width: float,
        height: float,
        depth: float,
        wall_thickness: float,
        has_mounting_flanges: bool,
        has_side_vents: bool,
        vent_count: int,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        # 1. Main outer casing & recessed inner tray
        casing_size = mathutils.Vector((width, height, depth))
        # Center of casing is at origin, but front face is at +depth/2
        casing_offset = mathutils.Vector((0.0, 0.0, depth / 2.0))

        MeshBuilder.add_recessed_tray(
            bm=bm,
            outer_size=casing_size,
            wall_thickness=wall_thickness,
            depth=depth * 0.15,
            offset=casing_offset,
            outer_mat_idx=mat_indices.get("casing", 0),
            outer_rgba=rgba_map.get("casing", (0.15, 0.15, 0.15, 1.0)),
            inner_mat_idx=mat_indices.get("casing_inner", 0),
            inner_rgba=rgba_map.get("casing_inner", (0.3, 0.3, 0.3, 1.0)),
            color_layer=color_layer
        )

        # 2. Mounting flanges (top and bottom ears for wall bolting)
        if has_mounting_flanges:
            flange_w = width * 0.8
            flange_h = 0.04
            flange_d = 0.015

            # Top flange
            top_offset = mathutils.Vector((
                0.0,
                (height / 2.0) + (flange_h / 2.0),
                flange_d / 2.0
            ))
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((flange_w, flange_h, flange_d)),
                offset=top_offset,
                mat_idx=mat_indices.get("mounting", 0),
                rgba=rgba_map.get("mounting", (0.2, 0.2, 0.2, 1.0)),
                color_layer=color_layer
            )

            # Bottom flange
            bottom_offset = mathutils.Vector((
                0.0,
                -(height / 2.0) - (flange_h / 2.0),
                flange_d / 2.0
            ))
            MeshBuilder.add_box(
                bm=bm,
                size=mathutils.Vector((flange_w, flange_h, flange_d)),
                offset=bottom_offset,
                mat_idx=mat_indices.get("mounting", 0),
                rgba=rgba_map.get("mounting", (0.2, 0.2, 0.2, 1.0)),
                color_layer=color_layer
            )

        # 3. Side vents / heat dissipation louvers (low-poly extruded slats)
        if has_side_vents and vent_count > 0:
            vent_w = depth * 0.45
            vent_h = 0.012
            vent_d = 0.008
            vent_start_y = height * 0.12

            for side in (-1.0, 1.0):
                for i in range(vent_count):
                    y_pos = vent_start_y - (i * 0.035)
                    vent_offset = mathutils.Vector((
                        side * ((width / 2.0) + (vent_d / 2.0)),
                        y_pos,
                        depth * 0.4
                    ))
                    MeshBuilder.add_box(
                        bm=bm,
                        size=mathutils.Vector((vent_d, vent_h, vent_w)),
                        offset=vent_offset,
                        mat_idx=mat_indices.get("casing", 0),
                        rgba=rgba_map.get("casing", (0.15, 0.15, 0.15, 1.0)),
                        color_layer=color_layer
                    )
