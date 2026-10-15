from typing import List, Tuple, Optional, Any
import math
import mathutils
import bmesh
from .texture_atlas import PS1TextureAtlas, Rect

class MeshBuilder:
    """Procedural geometry builder specializing in low-poly PSX style meshes with UV atlas mapping."""

    active_material_manager: Optional[Any] = None

    @classmethod
    def set_active_material_manager(cls, manager: Any):
        """Register the active MaterialManager for resolving material indices to texture atlas rects."""
        cls.active_material_manager = manager

    @classmethod
    def get_or_create_uv_layer(cls, bm: bmesh.types.BMesh) -> bmesh.types.BMLayerItem:
        """Ensure an active UV layer exists on the BMesh."""
        uv = bm.loops.layers.uv.get("UVMap")
        if not uv:
            uv = bm.loops.layers.uv.active
        if not uv:
            uv = bm.loops.layers.uv.new("UVMap")
        return uv

    @classmethod
    def get_or_create_color_layer(cls, bm: bmesh.types.BMesh) -> bmesh.types.BMLayerItem:
        """Ensure an active vertex color layer exists on the BMesh."""
        col = bm.loops.layers.color.get("Col")
        if not col:
            col = bm.loops.layers.color.get("Color")
        if not col:
            col = bm.loops.layers.color.active
        if not col:
            col = bm.loops.layers.color.new("Col")
        return col

    @classmethod
    def resolve_uv_rect(cls, mat_idx: int = 0, default_rect_name: str = "metal_dark_grime") -> Rect:
        """Resolve the appropriate texture atlas rectangle for a material slot index."""
        if cls.active_material_manager and hasattr(cls.active_material_manager, "get_rect_by_index"):
            return cls.active_material_manager.get_rect_by_index(mat_idx)
        return PS1TextureAtlas.get_rect(default_rect_name)

    @staticmethod
    def apply_face_attributes(
        face: bmesh.types.BMFace,
        mat_idx: int,
        rgba: Tuple[float, float, float, float],
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        smooth: bool = False
    ):
        """Assign material index, smooth shading flag, and vertex color to face loops."""
        face.material_index = mat_idx
        face.smooth = smooth
        if color_layer:
            for loop in face.loops:
                loop[color_layer] = rgba

    @staticmethod
    def apply_face_attributes_varied(
        face: bmesh.types.BMFace,
        mat_idx: int,
        base_rgba: Tuple[float, float, float, float],
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        component_id: int = 0,
        seed: int = 42,
        variation_amount: float = 0.06,
        smooth: bool = False
    ):
        """Assign material index, smooth shading flag, and component-varied vertex color to face loops."""
        face.material_index = mat_idx
        face.smooth = smooth
        if color_layer:
            if component_id != 0 and variation_amount > 0:
                import hashlib
                h_val = int(hashlib.md5(f"{seed}_{component_id}".encode()).hexdigest()[:6], 16)
                norm = (h_val % 1000) / 1000.0
                delta = (norm * 2.0 - 1.0) * variation_amount
                warmth = (((h_val >> 4) % 1000) / 1000.0) * 0.02
                rgba = (
                    min(1.0, max(0.0, base_rgba[0] * (1.0 + delta + warmth))),
                    min(1.0, max(0.0, base_rgba[1] * (1.0 + delta))),
                    min(1.0, max(0.0, base_rgba[2] * (1.0 + delta - warmth))),
                    base_rgba[3]
                )
            else:
                rgba = base_rgba
            for loop in face.loops:
                loop[color_layer] = rgba

    @staticmethod
    def apply_face_uv_rect(
        face: bmesh.types.BMFace,
        uv_layer: Optional[bmesh.types.BMLayerItem],
        uv_rect: Optional[Rect],
        inset_texels: float = 0.5
    ):
        """Map a quad or tri face's loops squarely into a UV rectangle (u0, v0, u1, v1) with sub-texel padding."""
        if not uv_layer or not uv_rect:
            return
        u0, v0, u1, v1 = uv_rect
        pad_u = min((inset_texels / 256.0), (u1 - u0) * 0.04)
        pad_v = min((inset_texels / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        loops = face.loops
        num_loops = len(loops)
        if num_loops == 4:
            loops[0][uv_layer].uv = (u0_p, v0_p)
            loops[1][uv_layer].uv = (u1_p, v0_p)
            loops[2][uv_layer].uv = (u1_p, v1_p)
            loops[3][uv_layer].uv = (u0_p, v1_p)
        elif num_loops == 3:
            loops[0][uv_layer].uv = (u0_p, v0_p)
            loops[1][uv_layer].uv = (u1_p, v0_p)
            loops[2][uv_layer].uv = ((u0_p + u1_p) * 0.5, v1_p)
        else:
            center_u = (u0_p + u1_p) * 0.5
            center_v = (v0_p + v1_p) * 0.5
            rad_u = (u1_p - u0_p) * 0.45
            rad_v = (v1_p - v0_p) * 0.45
            for i, loop in enumerate(loops):
                angle = (2.0 * math.pi * i) / num_loops
                loop[uv_layer].uv = (
                    center_u + math.cos(angle) * rad_u,
                    center_v + math.sin(angle) * rad_v
                )

    @classmethod
    def apply_box_face_uv(
        cls,
        face: bmesh.types.BMFace,
        uv_layer: Optional[bmesh.types.BMLayerItem],
        uv_rect: Optional[Rect],
        inset_texels: float = 0.5
    ):
        """
        Map a box face with orientation awareness:
        - Keeps vertical textures (grime gradients, dials, CRT lines, vent slats) upright along Z.
        - Maps top/bottom surfaces cleanly to X/Y.
        """
        if not uv_layer or not uv_rect:
            return
        u0, v0, u1, v1 = uv_rect
        pad_u = min((inset_texels / 256.0), (u1 - u0) * 0.04)
        pad_v = min((inset_texels / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        loops = face.loops
        if len(loops) != 4:
            cls.apply_face_uv_rect(face, uv_layer, (u0, v0, u1, v1), inset_texels=inset_texels)
            return

        normal = face.normal
        abs_x, abs_y, abs_z = abs(normal.x), abs(normal.y), abs(normal.z)

        if abs_z >= abs_x and abs_z >= abs_y:
            # Top/Bottom face (Normal ~ ±Z): Project X to U, Y to V
            xs = [l.vert.co.x for l in loops]
            ys = [l.vert.co.y for l in loops]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            span_x = max(1e-5, max_x - min_x)
            span_y = max(1e-5, max_y - min_y)
            for l in loops:
                tu = u0_p + ((l.vert.co.x - min_x) / span_x) * (u1_p - u0_p)
                tv = v0_p + ((l.vert.co.y - min_y) / span_y) * (v1_p - v0_p)
                l[uv_layer].uv = (tu, tv)
        elif abs_y >= abs_x:
            # Front/Back face (Normal ~ ±Y): Project X to U, Z to V (Z is UP)
            xs = [l.vert.co.x for l in loops]
            zs = [l.vert.co.z for l in loops]
            min_x, max_x = min(xs), max(xs)
            min_z, max_z = min(zs), max(zs)
            span_x = max(1e-5, max_x - min_x)
            span_z = max(1e-5, max_z - min_z)
            for l in loops:
                tu = u0_p + ((l.vert.co.x - min_x) / span_x) * (u1_p - u0_p)
                tv = v0_p + ((l.vert.co.z - min_z) / span_z) * (v1_p - v0_p)
                l[uv_layer].uv = (tu, tv)
        else:
            # Left/Right face (Normal ~ ±X): Project Y to U, Z to V (Z is UP)
            ys = [l.vert.co.y for l in loops]
            zs = [l.vert.co.z for l in loops]
            min_y, max_y = min(ys), max(ys)
            min_z, max_z = min(zs), max(zs)
            span_y = max(1e-5, max_y - min_y)
            span_z = max(1e-5, max_z - min_z)
            for l in loops:
                tu = u0_p + ((l.vert.co.y - min_y) / span_y) * (u1_p - u0_p)
                tv = v0_p + ((l.vert.co.z - min_z) / span_z) * (v1_p - v0_p)
                l[uv_layer].uv = (tu, tv)

    @classmethod
    def add_box(
        cls,
        bm: bmesh.types.BMesh,
        *args,
        size: Optional[Any] = None,
        offset: Optional[Any] = None,
        mat_idx: int = 0,
        rgba: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0),
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_rect: Optional[Rect] = None,
        **kwargs
    ) -> List[bmesh.types.BMFace]:
        """Create an axis-aligned box primitive with UV mapping into an atlas rect."""
        if len(args) >= 2:
            offset = args[0]
            size = args[1]
            if len(args) >= 3 and isinstance(args[2], int):
                mat_idx = args[2]
        elif len(args) == 1:
            if size is None:
                size = args[0]
            elif offset is None:
                offset = args[0]

        if "mat_idx" in kwargs:
            mat_idx = kwargs["mat_idx"]

        size_vec = mathutils.Vector(size) if size is not None else mathutils.Vector((1.0, 1.0, 1.0))
        offset_vec = mathutils.Vector(offset) if offset is not None else mathutils.Vector((0.0, 0.0, 0.0))

        geom = bmesh.ops.create_cube(bm, size=1.0)
        verts = [v for v in geom["verts"] if isinstance(v, bmesh.types.BMVert)]

        # Scale and position
        for v in verts:
            v.co.x = v.co.x * size_vec.x + offset_vec.x
            v.co.y = v.co.y * size_vec.y + offset_vec.y
            v.co.z = v.co.z * size_vec.z + offset_vec.z

        bm.faces.ensure_lookup_table()
        created_faces = []
        vert_set = set(verts)
        component_id = kwargs.get("component_id", 0)
        variation_seed = kwargs.get("seed", 42)
        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        uv_rect = uv_rect or cls.resolve_uv_rect(mat_idx, "metal_dark_grime")

        for f in bm.faces:
            if all(v in vert_set for v in f.verts):
                if component_id != 0:
                    cls.apply_face_attributes_varied(
                        f, mat_idx, rgba, color_layer,
                        component_id=component_id, seed=variation_seed,
                        variation_amount=variation_amount, smooth=False
                    )
                else:
                    cls.apply_face_attributes(f, mat_idx, rgba, color_layer, smooth=False)
                if uv_layer:
                    cls.apply_box_face_uv(f, uv_layer, uv_rect)
                created_faces.append(f)
        return created_faces

    @classmethod
    def add_recessed_tray(
        cls,
        bm: bmesh.types.BMesh,
        outer_size: mathutils.Vector,
        wall_thickness: float,
        depth: float,
        offset: mathutils.Vector,
        outer_mat_idx: int,
        outer_rgba: Tuple[float, float, float, float],
        inner_mat_idx: int,
        inner_rgba: Tuple[float, float, float, float],
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        outer_uv_rect: Optional[Rect] = None,
        inner_uv_rect: Optional[Rect] = None
    ):
        """Create a recessed industrial chassis tray with UV mapped outer and inner faces."""
        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        outer_uv_rect = outer_uv_rect or cls.resolve_uv_rect(outer_mat_idx, "metal_dark_grime")
        inner_uv_rect = inner_uv_rect or cls.resolve_uv_rect(inner_mat_idx, "metal_dark_grime")

        casing_faces = cls.add_box(
            bm,
            size=outer_size,
            offset=offset,
            mat_idx=outer_mat_idx,
            rgba=outer_rgba,
            color_layer=color_layer,
            uv_layer=uv_layer,
            uv_rect=outer_uv_rect
        )

        inner_w = max(0.05, outer_size.x - 2.0 * wall_thickness)
        inner_h = max(0.05, outer_size.y - 2.0 * wall_thickness)
        inner_d = depth

        inner_offset = mathutils.Vector((
            offset.x,
            offset.y,
            offset.z + (outer_size.z / 2.0) - (inner_d / 2.0) + 0.002
        ))

        inner_faces = cls.add_box(
            bm,
            size=mathutils.Vector((inner_w, inner_h, inner_d)),
            offset=inner_offset,
            mat_idx=inner_mat_idx,
            rgba=inner_rgba,
            color_layer=color_layer,
            uv_layer=uv_layer,
            uv_rect=inner_uv_rect
        )
        return casing_faces + inner_faces

    @classmethod
    def add_cylinder(
        cls,
        bm: bmesh.types.BMesh,
        *args,
        radius: float = 0.5,
        depth: float = 1.0,
        segments: Optional[int] = None,
        offset: Optional[Any] = None,
        axis: str = 'Z',
        mat_idx: int = 0,
        rgba: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0),
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_rect: Optional[Rect] = None,
        smooth: bool = False,
        **kwargs
    ) -> List[bmesh.types.BMFace]:
        """Create a low-poly cylinder aligned along X, Y, or Z with cylindrical UV wrapping."""
        if len(args) > 0:
            if isinstance(args[0], (tuple, list, mathutils.Vector)):
                offset = args[0]
                if len(args) > 1:
                    radius = float(args[1])
                if len(args) > 2:
                    depth = float(args[2])
            else:
                radius = float(args[0])
                if len(args) > 1:
                    depth = float(args[1])
                if len(args) > 2:
                    segments = int(args[2])
                if len(args) > 3:
                    offset = args[3]

        if segments is None:
            segments = int(kwargs.get("sides", kwargs.get("segments", 8)))
        if "sides" in kwargs:
            segments = int(kwargs["sides"])
        if "axis" in kwargs:
            axis = kwargs["axis"]
        if "mat_idx" in kwargs:
            mat_idx = kwargs["mat_idx"]

        offset_vec = mathutils.Vector(offset) if offset is not None else mathutils.Vector((0.0, 0.0, 0.0))
        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        uv_rect = uv_rect or cls.resolve_uv_rect(mat_idx, "metal_light_brushed")

        geom = bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=segments,
            radius1=radius,
            radius2=radius,
            depth=depth
        )
        verts = [v for v in geom["verts"] if isinstance(v, bmesh.types.BMVert)]

        if axis == 'X':
            rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')
            for v in verts:
                v.co = rot @ v.co
        elif axis == 'Y':
            rot = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
            for v in verts:
                v.co = rot @ v.co

        for v in verts:
            v.co += offset_vec

        bm.faces.ensure_lookup_table()
        vert_set = set(verts)
        created_faces = []

        # UV mapping coordinates with padding
        u0, v0, u1, v1 = uv_rect
        pad_u = min((0.5 / 256.0), (u1 - u0) * 0.04)
        pad_v = min((0.5 / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        center_u = (u0_p + u1_p) * 0.5
        center_v = (v0_p + v1_p) * 0.5
        rad_u = (u1_p - u0_p) * 0.45
        rad_v = (v1_p - v0_p) * 0.45

        for f in bm.faces:
            if all(v in vert_set for v in f.verts):
                cls.apply_face_attributes(f, mat_idx, rgba, color_layer, smooth=smooth)
                if uv_layer:
                    if len(f.verts) == 4:
                        # Side quad
                        cls.apply_face_uv_rect(f, uv_layer, (u0, v0, u1, v1))
                    else:
                        # End cap
                        for i, loop in enumerate(f.loops):
                            ang = (2.0 * math.pi * i) / len(f.loops)
                            loop[uv_layer].uv = (
                                center_u + math.cos(ang) * rad_u,
                                center_v + math.sin(ang) * rad_v
                            )
                created_faces.append(f)
        return created_faces

    @classmethod
    def add_circle(
        cls,
        bm: bmesh.types.BMesh,
        *args,
        radius: float = 0.5,
        segments: Optional[int] = None,
        offset: Optional[Any] = None,
        axis: str = 'Z',
        mat_idx: int = 0,
        rgba: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0),
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_rect: Optional[Rect] = None,
        smooth: bool = False,
        **kwargs
    ) -> List[bmesh.types.BMFace]:
        """Create a flat circular or polygon face aligned to an axis with circular UV mapping."""
        if len(args) > 0:
            if isinstance(args[0], (tuple, list, mathutils.Vector)):
                offset = args[0]
                if len(args) > 1:
                    radius = float(args[1])
            else:
                radius = float(args[0])
                if len(args) > 1:
                    segments = int(args[1])
                if len(args) > 2:
                    offset = args[2]

        if segments is None:
            segments = int(kwargs.get("sides", kwargs.get("segments", 8)))
        if "sides" in kwargs:
            segments = int(kwargs["sides"])
        if "axis" in kwargs:
            axis = kwargs["axis"]
        if "mat_idx" in kwargs:
            mat_idx = kwargs["mat_idx"]

        offset_vec = mathutils.Vector(offset) if offset is not None else mathutils.Vector((0.0, 0.0, 0.0))
        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        uv_rect = uv_rect or cls.resolve_uv_rect(mat_idx, "metal_light_brushed")

        geom = bmesh.ops.create_circle(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=segments,
            radius=radius
        )
        verts = [v for v in geom["verts"] if isinstance(v, bmesh.types.BMVert)]

        if axis == 'X':
            rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')
            for v in verts:
                v.co = rot @ v.co
        elif axis == 'Y':
            rot = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
            for v in verts:
                v.co = rot @ v.co

        for v in verts:
            v.co += offset_vec

        bm.faces.ensure_lookup_table()
        vert_set = set(verts)
        created_faces = []

        u0, v0, u1, v1 = uv_rect
        pad_u = min((0.5 / 256.0), (u1 - u0) * 0.04)
        pad_v = min((0.5 / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        center_u = (u0_p + u1_p) * 0.5
        center_v = (v0_p + v1_p) * 0.5
        rad_u = (u1_p - u0_p) * 0.45
        rad_v = (v1_p - v0_p) * 0.45

        for f in bm.faces:
            if all(v in vert_set for v in f.verts):
                cls.apply_face_attributes(f, mat_idx, rgba, color_layer, smooth=smooth)
                if uv_layer:
                    for i, loop in enumerate(f.loops):
                        ang = (2.0 * math.pi * i) / len(f.loops)
                        loop[uv_layer].uv = (
                            center_u + math.cos(ang) * rad_u,
                            center_v + math.sin(ang) * rad_v
                        )
                created_faces.append(f)
        return created_faces

    @classmethod
    def add_crt_screen(
        cls,
        bm: bmesh.types.BMesh,
        width: float,
        height: float,
        bulge: float,
        offset: mathutils.Vector,
        screen_mat_idx: int,
        screen_rgba: Tuple[float, float, float, float],
        frame_mat_idx: int,
        frame_rgba: Tuple[float, float, float, float],
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        screen_uv_rect: Optional[Rect] = None,
        frame_uv_rect: Optional[Rect] = None
    ):
        """Create a classic low-poly PSX CRT screen with seamless screen grid UV mapping."""
        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        screen_uv_rect = screen_uv_rect or cls.resolve_uv_rect(screen_mat_idx, "crt_screen_green")
        frame_uv_rect = frame_uv_rect or cls.resolve_uv_rect(frame_mat_idx, "beige_plastic_worn")

        # 1. Bezel frame box
        frame_margin = min(width, height) * 0.12
        frame_size = mathutils.Vector((width + frame_margin * 2, height + frame_margin * 2, 0.04))
        cls.add_box(
            bm,
            size=frame_size,
            offset=offset,
            mat_idx=frame_mat_idx,
            rgba=frame_rgba,
            color_layer=color_layer,
            uv_layer=uv_layer,
            uv_rect=frame_uv_rect
        )

        # 2. CRT Glass Grid (3x3 grid = 9 quads, 18 tris)
        rows, cols = 3, 3
        dx = width / cols
        dy = height / rows
        half_w = width / 2.0
        half_h = height / 2.0
        z_base = offset.z + 0.02

        u0, v0, u1, v1 = screen_uv_rect
        pad_u = min((0.5 / 256.0), (u1 - u0) * 0.04)
        pad_v = min((0.5 / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        grid_verts = []
        for r in range(rows + 1):
            row_list = []
            for c in range(cols + 1):
                x = -half_w + c * dx + offset.x
                y = -half_h + r * dy + offset.y
                nx = (c / cols - 0.5) * 2.0
                ny = (r / rows - 0.5) * 2.0
                dist_sq = nx * nx + ny * ny
                z_bulge = max(0.0, 1.0 - dist_sq * 0.5) * bulge

                v = bm.verts.new((x, y, z_base + z_bulge))
                row_list.append(v)
            grid_verts.append(row_list)

        bm.verts.ensure_lookup_table()
        for r in range(rows):
            for c in range(cols):
                v0_vert = grid_verts[r][c]
                v1_vert = grid_verts[r][c + 1]
                v2_vert = grid_verts[r + 1][c + 1]
                v3_vert = grid_verts[r + 1][c]
                f = bm.faces.new((v0_vert, v1_vert, v2_vert, v3_vert))
                cls.apply_face_attributes(f, screen_mat_idx, screen_rgba, color_layer, smooth=True)

                if uv_layer:
                    # UV sub-rect for this grid cell
                    cu0 = u0_p + (c / cols) * (u1_p - u0_p)
                    cu1 = u0_p + ((c + 1) / cols) * (u1_p - u0_p)
                    cv0 = v0_p + (r / rows) * (v1_p - v0_p)
                    cv1 = v0_p + ((r + 1) / rows) * (v1_p - v0_p)
                    f.loops[0][uv_layer].uv = (cu0, cv0)
                    f.loops[1][uv_layer].uv = (cu1, cv0)
                    f.loops[2][uv_layer].uv = (cu1, cv1)
                    f.loops[3][uv_layer].uv = (cu0, cv1)

    @classmethod
    def add_extruded_cable(
        cls,
        bm: bmesh.types.BMesh,
        points: List[Any],
        radius: float = 0.012,
        sides: int = 4,
        mat_idx: int = 0,
        rgba: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0),
        color_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_layer: Optional[bmesh.types.BMLayerItem] = None,
        uv_rect: Optional[Rect] = None,
        **kwargs
    ):
        """Extrude an N-sided tube along path points with UV mapping."""
        if "sides" in kwargs:
            sides = int(kwargs["sides"])
        if "mat_idx" in kwargs:
            mat_idx = int(kwargs["mat_idx"])
        if "radius" in kwargs:
            radius = float(kwargs["radius"])

        uv_layer = uv_layer or cls.get_or_create_uv_layer(bm)
        color_layer = color_layer or cls.get_or_create_color_layer(bm)
        uv_rect = uv_rect or cls.resolve_uv_rect(mat_idx, "rubber_black")

        pts = [mathutils.Vector(p) for p in points]
        if len(pts) < 2:
            return

        rings = []
        angle_step = (2.0 * math.pi) / sides

        for i, pt in enumerate(pts):
            if i == 0:
                tangent = (pts[1] - pt).normalized()
            elif i == len(pts) - 1:
                tangent = (pt - pts[i - 1]).normalized()
            else:
                tangent = (pts[i + 1] - pts[i - 1]).normalized()

            arbitrary = mathutils.Vector((0, 0, 1)) if abs(tangent.z) < 0.9 else mathutils.Vector((1, 0, 0))
            normal = tangent.cross(arbitrary).normalized()
            binormal = tangent.cross(normal).normalized()

            ring_verts = []
            for s in range(sides):
                angle = s * angle_step
                offset = (normal * math.cos(angle) + binormal * math.sin(angle)) * radius
                v = bm.verts.new(pt + offset)
                ring_verts.append(v)
            rings.append(ring_verts)

        bm.verts.ensure_lookup_table()
        u0, v0, u1, v1 = uv_rect
        pad_u = min((0.5 / 256.0), (u1 - u0) * 0.04)
        pad_v = min((0.5 / 256.0), (v1 - v0) * 0.04)
        u0_p = u0 + pad_u
        u1_p = u1 - pad_u
        v0_p = v0 + pad_v
        v1_p = v1 - pad_v

        num_segments = len(rings) - 1

        for i in range(num_segments):
            r0 = rings[i]
            r1 = rings[i + 1]
            seg_v0 = v0_p + (i / num_segments) * (v1_p - v0_p)
            seg_v1 = v0_p + ((i + 1) / num_segments) * (v1_p - v0_p)

            for s in range(sides):
                next_s = (s + 1) % sides
                v0_v = r0[s]
                v1_v = r0[next_s]
                v2_v = r1[next_s]
                v3_v = r1[s]
                f = bm.faces.new((v0_v, v1_v, v2_v, v3_v))
                cls.apply_face_attributes(f, mat_idx, rgba, color_layer, smooth=False)

                if uv_layer:
                    seg_u0 = u0_p + (s / sides) * (u1_p - u0_p)
                    seg_u1 = u0_p + ((s + 1) / sides) * (u1_p - u0_p)
                    f.loops[0][uv_layer].uv = (seg_u0, seg_v0)
                    f.loops[1][uv_layer].uv = (seg_u1, seg_v0)
                    f.loops[2][uv_layer].uv = (seg_u1, seg_v1)
                    f.loops[3][uv_layer].uv = (seg_u0, seg_v1)

        f_start = bm.faces.new(reversed(rings[0]))
        f_end = bm.faces.new(rings[-1])
        cls.apply_face_attributes(f_start, mat_idx, rgba, color_layer, smooth=False)
        cls.apply_face_attributes(f_end, mat_idx, rgba, color_layer, smooth=False)
        if uv_layer:
            cls.apply_face_uv_rect(f_start, uv_layer, (u0, v0, u1, v1))
            cls.apply_face_uv_rect(f_end, uv_layer, (u0, v0, u1, v1))
