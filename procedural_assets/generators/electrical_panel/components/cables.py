import mathutils
import bmesh
from typing import Optional, List
import random
from ....core.mesh_builder import MeshBuilder
from ....core.transform_utils import generate_catenary_cable_points

class CablesComponent:
    """Generates industrial conduit glands and hanging low-poly umbilical cables."""

    @classmethod
    def build(
        cls,
        bm: bmesh.types.BMesh,
        bottom_pos: mathutils.Vector,
        count: int,
        panel_w: float,
        panel_h: float,
        cable_sides: int,
        curve_segments: int,
        rng: random.Random,
        mat_indices: dict,
        color_layer: Optional[bmesh.types.BMLayerItem],
        rgba_map: dict
    ):
        if count <= 0:
            return

        cable_materials = ["cable_black", "cable_hazard", "cable_red"]
        gland_radius = 0.022
        gland_depth = 0.03
        cable_radius = 0.012

        spacing = min(panel_w * 0.25, 0.08)
        start_x = bottom_pos.x - ((count - 1) * spacing / 2.0)

        for i in range(count):
            gx = start_x + (i * spacing)
            gy = bottom_pos.y
            gz = bottom_pos.z

            gland_center = mathutils.Vector((gx, gy, gz))

            # 1. Cable gland / threaded conduit socket at bottom of chassis
            MeshBuilder.add_cylinder(
                bm=bm,
                radius=gland_radius,
                depth=gland_depth,
                segments=max(4, cable_sides),
                offset=gland_center,
                axis='Y',  # pointing downwards
                mat_idx=mat_indices.get("switch_base", 0),
                rgba=rgba_map.get("switch_base", (0.1, 0.1, 0.1, 1.0)),
                color_layer=color_layer,
                smooth=False
            )

            # 2. Hanging cable path
            cable_start = mathutils.Vector((gx, gy - (gland_depth / 2.0), gz))
            
            # Destination: hanging downwards and slightly toward the back/wall or looping
            hang_dist = panel_h * rng.uniform(0.35, 0.55)
            drift_x = rng.uniform(-0.06, 0.06)
            cable_end = mathutils.Vector((
                gx + drift_x,
                gy - hang_dist,
                gz - 0.05
            ))

            sag = rng.uniform(0.04, 0.09)
            cable_pts = generate_catenary_cable_points(
                start=cable_start,
                end=cable_end,
                segments=curve_segments,
                sag=sag,
                side_drift=drift_x * 0.5
            )

            mat_choice = rng.choice(cable_materials)
            MeshBuilder.add_extruded_cable(
                bm=bm,
                points=cable_pts,
                radius=cable_radius,
                sides=cable_sides,
                mat_idx=mat_indices.get(mat_choice, 0),
                rgba=rgba_map.get(mat_choice, (0.1, 0.1, 0.1, 1.0)),
                color_layer=color_layer
            )
