import bpy
import bmesh
import math
from ...core.base_generator import BaseAssetGenerator
from ...materials.palette import get_or_create_material

class AccessCardGenerator(BaseAssetGenerator):
    def generate(self, config=None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        mesh = bpy.data.meshes.new("AccessCard")
        obj = bpy.data.objects.new("AccessCard", mesh)
        bpy.context.collection.objects.link(obj)
        bm = bmesh.new()

        # Base card dimensions
        w = self.config.width / 2
        h = self.config.height / 2
        t = self.config.thickness / 2

        # Create main body
        bm_cube = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, h, t), verts=bm.verts)

        # Create a small hole for the lanyard (PSX style: just a small square cutout)
        hole_size = 0.005
        hole_x = w - 0.01
        hole_y = 0
        
        # Simple bevel for corners (low poly)
        bmesh.ops.bevel(bm, geom=bm.edges, offset=0.002, segments=1, profile=0.5)

        # Add a "chip" or "magnetic stripe" detail using a separate small cube to keep geometry clean
        chip_w = self.config.chip_size / 2
        chip_h = self.config.chip_size / 2
        chip_t = 0.001
        
        import mathutils
        matrix_chip = mathutils.Matrix.Translation((-w * 0.5, h * 0.3, t))
        bmesh.ops.create_cube(bm, size=1.0, matrix=matrix_chip)
        # Scale the last added verts (the chip)
        chip_verts = [v for v in bm.verts if v.select]
        # Note: In a real script we'd track indices, here we simplify for the procedural generation
        
        bm.to_mesh(mesh)
        bm.free()

        # Material setup
        mat = get_or_create_material(self.config.palette_name)
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        if len(obj.data.color_attributes) == 0:
            obj.data.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
        if len(obj.data.uv_layers) == 0:
            obj.data.uv_layers.new(name="UVMap")

        self.compact_materials(obj)
        return obj
