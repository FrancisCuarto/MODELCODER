import bpy
import bmesh
import mathutils
from ...core.base_generator import BaseAssetGenerator
from ...core.mesh_builder import MeshBuilder
from ...core.texture_atlas import PS1TextureAtlas

class AccessCardGenerator(BaseAssetGenerator):
    """
    Procedural keycard generator with PSX aesthetics, security badge stripes,
    microchip contact pads and magnetic stripe.
    """

    def generate(self, config=None) -> bpy.types.Object:
        if config is not None:
            self.config = config
        self.clean_context()
        self.material_manager = self.get_material_manager(self.config)
        MeshBuilder.set_active_material_manager(self.material_manager)

        mesh = bpy.data.meshes.new("AccessCard")
        obj = bpy.data.objects.new("AccessCard", mesh)
        bpy.context.collection.objects.link(obj)

        self.material_manager.assign_to_mesh(obj)
        m_idx = self.material_manager.material_indices

        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new("UVMap")
        col_layer = bm.loops.layers.color.new("Col")

        w = self.config.width / 2.0
        h = self.config.height / 2.0
        t = self.config.thickness / 2.0

        # Card body (white retro composite plastic)
        card_rect = PS1TextureAtlas.get_rect("painted_metal_white")
        card_mat = m_idx.get("casing", 0)
        card_rgba = (0.88, 0.90, 0.92, 1.0)

        # Base card
        res = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, h, t), verts=bm.verts)

        for face in list(bm.faces):
            if abs(face.normal.z) > 0.5:
                MeshBuilder.apply_face_attributes(face, card_mat, card_rgba, col_layer)
                MeshBuilder.apply_face_uv_rect(face, uv_layer, card_rect)
            else:
                edge_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
                MeshBuilder.apply_face_attributes(face, card_mat, (0.45, 0.45, 0.50, 1.0), col_layer)
                MeshBuilder.apply_face_uv_rect(face, uv_layer, edge_rect)

        # Security level indicator header band
        header_h = h * 0.35
        header_mat = m_idx.get("hazard_yellow", m_idx.get("sign_caution", 0))
        header_rect = PS1TextureAtlas.get_rect("caution_label")
        header_trans = mathutils.Matrix.Translation((0.0, h - header_h / 2.0, t + 0.0002))
        h_cube = bmesh.ops.create_cube(bm, size=1.0, matrix=header_trans)
        h_verts = list(h_cube["verts"])
        bmesh.ops.scale(bm, vec=(w * 0.95, header_h / 2.0, 0.0002), verts=h_verts)
        for face in [f for f in bm.faces if any(v in h_verts for v in f.verts)]:
            MeshBuilder.apply_face_attributes(face, header_mat, (0.92, 0.78, 0.12, 1.0), col_layer)
            MeshBuilder.apply_face_uv_rect(face, uv_layer, header_rect)

        # Golden security microchip
        chip_size = getattr(self.config, "chip_size", 0.014)
        chip_mat = m_idx.get("brass", m_idx.get("casing", 0))
        chip_rect = PS1TextureAtlas.get_rect("cartridge_amber")
        chip_trans = mathutils.Matrix.Translation((-w * 0.4, -h * 0.15, t + 0.0004))
        c_cube = bmesh.ops.create_cube(bm, size=1.0, matrix=chip_trans)
        c_verts = list(c_cube["verts"])
        bmesh.ops.scale(bm, vec=(chip_size / 2.0, chip_size / 2.0, 0.0002), verts=c_verts)
        for face in [f for f in bm.faces if any(v in c_verts for v in f.verts)]:
            MeshBuilder.apply_face_attributes(face, chip_mat, (0.88, 0.68, 0.18, 1.0), col_layer)
            MeshBuilder.apply_face_uv_rect(face, uv_layer, chip_rect)

        # Magnetic stripe on the back
        mag_rect = PS1TextureAtlas.get_rect("metal_dark_grime")
        mag_mat = m_idx.get("dark_metal", m_idx.get("casing", 0))
        mag_trans = mathutils.Matrix.Translation((0.0, h * 0.4, -(t + 0.0003)))
        m_cube = bmesh.ops.create_cube(bm, size=1.0, matrix=mag_trans)
        m_verts = list(m_cube["verts"])
        bmesh.ops.scale(bm, vec=(w, h * 0.22, 0.0002), verts=m_verts)
        for face in [f for f in bm.faces if any(v in m_verts for v in f.verts)]:
            MeshBuilder.apply_face_attributes(face, mag_mat, (0.12, 0.12, 0.14, 1.0), col_layer)
            MeshBuilder.apply_face_uv_rect(face, uv_layer, mag_rect)

        bm.to_mesh(mesh)
        bm.free()

        self.compact_materials(obj)
        return obj
