from typing import Tuple, List, Optional
import math
import mathutils
import bmesh
import bpy

def count_triangles(bm: bmesh.types.BMesh) -> int:
    """Calculate the total triangle count of a BMesh."""
    return sum(len(f.verts) - 2 for f in bm.faces)

def get_mesh_bounds(bm: bmesh.types.BMesh) -> Tuple[mathutils.Vector, mathutils.Vector, mathutils.Vector]:
    """Calculate min_coords, max_coords, and dimensions (width, height, depth) for a BMesh."""
    if not bm.verts:
        zero = mathutils.Vector((0, 0, 0))
        return zero, zero, zero

    min_co = mathutils.Vector((float('inf'), float('inf'), float('inf')))
    max_co = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))

    for v in bm.verts:
        min_co.x = min(min_co.x, v.co.x)
        min_co.y = min(min_co.y, v.co.y)
        min_co.z = min(min_co.z, v.co.z)
        max_co.x = max(max_co.x, v.co.x)
        max_co.y = max(max_co.y, v.co.y)
        max_co.z = max(max_co.z, v.co.z)

    dims = max_co - min_co
    return min_co, max_co, dims

def rotate_point(p: mathutils.Vector, axis: str, angle_rad: float) -> mathutils.Vector:
    """Rotate a point around X, Y, or Z axis."""
    rot = mathutils.Matrix.Rotation(angle_rad, 4, axis)
    p_4d = p.to_4d()
    rotated = rot @ p_4d
    return rotated.to_3d()

def generate_catenary_cable_points(
    start: mathutils.Vector,
    end: mathutils.Vector,
    segments: int = 5,
    sag: float = 0.15,
    side_drift: float = 0.0
) -> List[mathutils.Vector]:
    """
    Generate points along a naturally hanging / draped cable between start and end.
    Uses a parabolic approximation of a catenary curve for low-poly performance.
    """
    points = []
    for i in range(segments + 1):
        t = i / float(segments)
        # Linear interpolation between start and end
        interp = start.lerp(end, t)
        
        # Parabolic sag: 4 * t * (1 - t) peaks at t=0.5 with value 1.0
        h_sag = 4.0 * t * (1.0 - t) * sag
        drift = 4.0 * t * (1.0 - t) * side_drift

        pt = mathutils.Vector((
            interp.x + drift,
            interp.y,
            interp.z - h_sag
        ))
        points.append(pt)
    return points
