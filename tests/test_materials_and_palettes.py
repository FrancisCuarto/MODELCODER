import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
import bmesh
from mathutils import Vector

from procedural_assets.core.materials import (
    MaterialManager,
    MaterialCategory,
    MaterialRole,
    MaterialDef,
    DEFAULT_PALETTES,
    PALETTE_ROLE_MAP,
)
from procedural_assets.core.texture_atlas import PS1TextureAtlas
from procedural_assets.generators.electrical_panel.config import ElectricalPanelConfig
from procedural_assets.generators.electrical_panel.generator import ElectricalPanelGenerator
from procedural_assets.generators.crash_cart.config import CrashCartConfig
from procedural_assets.generators.crash_cart.generator import CrashCartGenerator
from procedural_assets.generators.scrub_sink.config import ScrubSinkConfig
from procedural_assets.generators.scrub_sink.generator import ScrubSinkGenerator
from procedural_assets.generators.autopsy_table.config import AutopsyTableConfig
from procedural_assets.generators.autopsy_table.generator import AutopsyTableGenerator
from procedural_assets.generators.crate.config import CrateConfig
from procedural_assets.generators.crate.generator import CrateGenerator
from procedural_assets.generators.terminal.config import TerminalConfig
from procedural_assets.generators.terminal.generator import TerminalGenerator
from procedural_assets.export.glb_exporter import GLBExporter

class TestMaterialsAndPalettes(unittest.TestCase):
    """Unit test suite verifying the PSX procedural material and palette system for Below Nominal."""

    def setUp(self):
        # Clean existing test meshes and materials before each test
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in list(bpy.data.meshes):
            bpy.data.meshes.remove(mesh, do_unlink=True)
        for mat in list(bpy.data.materials):
            bpy.data.materials.remove(mat, do_unlink=True)

    def test_default_palettes_exist_and_complete(self):
        """Verify all 5 thematic sector palettes exist and contain required base materials."""
        expected_palettes = [
            "industrial_hazard",
            "medbay_clean",
            "command_bridge",
            "habitation_worn",
            "derelict_decay"
        ]
        for pal_name in expected_palettes:
            self.assertIn(pal_name, DEFAULT_PALETTES, f"Palette '{pal_name}' missing from DEFAULT_PALETTES")
            pal = DEFAULT_PALETTES[pal_name]
            self.assertGreaterEqual(len(pal), 10, f"Palette '{pal_name}' should have at least 10 material definitions")

    def test_material_categories_and_pbr_calibration(self):
        """Verify calibrated roughness and metallic properties across 6 core material categories."""
        mgr = MaterialManager(palette_name="medbay_clean", wear_level=0.5, seed=42)

        # 1. Glazed ceramic (ceramic_white)
        self.assertIn("ceramic_white", mgr.palette)
        mat_ceramic = mgr.palette["ceramic_white"]
        self.assertEqual(mat_ceramic.category, MaterialCategory.CERAMIC)
        self.assertEqual(mat_ceramic.metallic, 0.0)
        self.assertLessEqual(mat_ceramic.roughness, 0.35)

        # 2. Bare / Stainless steel (steel_brushed)
        self.assertIn("steel_brushed", mgr.palette)
        mat_steel = mgr.palette["steel_brushed"]
        self.assertEqual(mat_steel.category, MaterialCategory.STEEL)
        self.assertGreaterEqual(mat_steel.metallic, 0.8)
        self.assertLessEqual(mat_steel.roughness, 0.45)

        # 3. Translucent safety glass (glass_tube / glass_reinforced)
        self.assertIn("glass_tube", mgr.palette)
        mat_glass = mgr.palette["glass_tube"]
        self.assertEqual(mat_glass.category, MaterialCategory.GLASS)
        self.assertGreaterEqual(mat_glass.transmission, 0.8)
        self.assertEqual(mat_glass.metallic, 0.05)

        # 4. Painted clinical enamel (casing)
        self.assertIn("casing", mgr.palette)
        mat_paint = mgr.palette["casing"]
        self.assertEqual(mat_paint.category, MaterialCategory.PAINTED_METAL)
        self.assertLessEqual(mat_paint.metallic, 0.15)
        self.assertGreaterEqual(mat_paint.roughness, 0.45)

        # 5. Emissive telemetry screen (crt_screen)
        self.assertIn("crt_screen", mgr.palette)
        mat_screen = mgr.palette["crt_screen"]
        self.assertEqual(mat_screen.category, MaterialCategory.SCREEN)
        self.assertIsNotNone(mat_screen.emission_color)
        self.assertGreater(mat_screen.emission_strength, 0.0)

        # 6. Industrial plastic (crt_frame in habitation_worn)
        mgr_hab = MaterialManager(palette_name="habitation_worn")
        self.assertIn("crt_frame", mgr_hab.palette)
        mat_plastic = mgr_hab.palette["crt_frame"]
        self.assertEqual(mat_plastic.category, MaterialCategory.PLASTIC)
        self.assertEqual(mat_plastic.metallic, 0.02)
        self.assertGreaterEqual(mat_plastic.roughness, 0.4)

    def test_semantic_role_resolution(self):
        """Verify semantic roles resolve to palette-specific material keys."""
        mgr_med = MaterialManager(palette_name="medbay_clean")
        mgr_cmd = MaterialManager(palette_name="command_bridge")
        mgr_ind = MaterialManager(palette_name="industrial_hazard")

        # Screen role
        self.assertEqual(mgr_med.resolve_key(MaterialRole.SCREEN), "crt_screen")
        self.assertEqual(mgr_cmd.resolve_key(MaterialRole.SCREEN), "crt_screen")
        self.assertEqual(mgr_ind.resolve_key(MaterialRole.SCREEN), "crt_screen")

        # Verify screens in different palettes have distinct sector emission colors
        self.assertNotEqual(mgr_med.palette["crt_screen"].emission_color, mgr_cmd.palette["crt_screen"].emission_color)
        self.assertNotEqual(mgr_med.palette["crt_screen"].emission_color, mgr_ind.palette["crt_screen"].emission_color)

        # Ceramic role
        self.assertEqual(mgr_med.resolve_key(MaterialRole.CERAMIC), "ceramic_white")

        # Glass role
        self.assertEqual(mgr_med.resolve_key(MaterialRole.GLASS), "glass_tube")
        self.assertEqual(mgr_cmd.resolve_key(MaterialRole.GLASS), "glass_observation")

        # Casing role
        self.assertEqual(mgr_med.resolve_key(MaterialRole.CASING), "casing")
        self.assertEqual(mgr_cmd.resolve_key(MaterialRole.CASING), "casing")
        self.assertEqual(mgr_ind.resolve_key(MaterialRole.CASING), "casing")

        # Frame role
        self.assertEqual(mgr_med.resolve_key(MaterialRole.FRAME), "mounting")

    def test_component_rgba_variation(self):
        """Verify deterministic color variation between different component IDs."""
        mgr = MaterialManager(palette_name="industrial_hazard")
        casing_rgba = mgr.get_rgba("painted_casing")

        # Base color without component modulation
        var0 = mgr.get_component_rgba("painted_casing", component_id=0, variation_amount=0.07)
        var1 = mgr.get_component_rgba("painted_casing", component_id=1, variation_amount=0.07)
        var2 = mgr.get_component_rgba("painted_casing", component_id=2, variation_amount=0.07)

        # Must differ from each other
        self.assertNotEqual(var0, var1)
        self.assertNotEqual(var1, var2)

        # Deterministic: repeated call for same component_id produces exact same tuple
        var0_repeat = mgr.get_component_rgba("painted_casing", component_id=0, variation_amount=0.07)
        self.assertEqual(var0, var0_repeat)

        # Alpha channel must remain 1.0
        self.assertEqual(var0[3], 1.0)
        self.assertEqual(var1[3], 1.0)

        # Variations must remain within reasonable bounds of base color
        for c, v in zip(casing_rgba[:3], var0[:3]):
            self.assertAlmostEqual(c, v, delta=0.15)

    def test_configurable_emission_scale(self):
        """Verify emission_scale scales the Principled BSDF emission strength."""
        mgr_normal = MaterialManager(palette_name="industrial_hazard", emission_multiplier=1.0)
        mat_normal = mgr_normal.get_or_create_material("screen_green")
        bsdf_normal = [n for n in mat_normal.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
        strength_normal = bsdf_normal.inputs["Emission Strength"].default_value

        # Clean materials to avoid cache hit
        bpy.data.materials.remove(mat_normal, do_unlink=True)

        mgr_boosted = MaterialManager(palette_name="industrial_hazard", emission_multiplier=3.0)
        mat_boosted = mgr_boosted.get_or_create_material("screen_green")
        bsdf_boosted = [n for n in mat_boosted.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
        strength_boosted = bsdf_boosted.inputs["Emission Strength"].default_value

        self.assertAlmostEqual(strength_boosted, strength_normal * 3.0, places=3)

    def test_material_deduplication_and_stable_naming(self):
        """Verify get_or_create_material reuses materials without generating Material.001 duplicates."""
        mgr = MaterialManager(palette_name="medbay_clean", wear_level=0.5, seed=42)

        mat1 = mgr.get_or_create_material("steel_stainless")
        mat2 = mgr.get_or_create_material("steel_stainless")

        # Stable naming format: mat_psx_{palette}_{key}_w{wear}
        self.assertEqual(mat1.name, "mat_psx_medbay_clean_steel_stainless_w50")
        # Must be identical object pointer (no duplicate created)
        self.assertIs(mat1, mat2)

        # Only 1 material exists in Blender data
        matching = [m for m in bpy.data.materials if m.name.startswith("mat_psx_medbay_clean_steel_stainless")]
        self.assertEqual(len(matching), 1)

    def test_texture_sampling_is_point_closest(self):
        """Verify texture node is set to Closest (point) sampling for authentic PSX look."""
        mgr = MaterialManager(palette_name="industrial_hazard")
        mat = mgr.get_or_create_material("painted_casing")
        tex_node = [n for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"][0]
        self.assertEqual(tex_node.interpolation, "Closest")

    def test_material_compaction_on_generator(self):
        """Verify that compact_materials purges unused material slots upon generation."""
        cfg = ElectricalPanelConfig(
            name="test_panel_compact",
            palette_name="medbay_clean",
            wear_level=0.4
        )
        gen = ElectricalPanelGenerator()
        obj = gen.generate(cfg)
        gen.validate(obj, cfg)

        # Before compaction, an asset holds all 51 palette slots.
        # After compaction, it must only hold slots that are actually referenced by its polygons.
        assigned_slots = len(obj.material_slots)
        self.assertGreater(assigned_slots, 0, "Object should have at least 1 material slot")
        self.assertLess(assigned_slots, len(DEFAULT_PALETTES["medbay_clean"]), "Compacted object must drop unused slots")

        # Verify that EVERY slot on the object is actively used by at least one face (no unused/empty slots)
        used_indices = set(poly.material_index for poly in obj.data.polygons)
        self.assertEqual(len(used_indices), assigned_slots, "Every slot must be used by at least one polygon")
        self.assertEqual(used_indices, set(range(assigned_slots)), "Polygon material indices must be contiguous 0..N-1")

    def test_gltf_export_with_compact_materials(self):
        """Verify export to GLB runs without error and creates a valid asset file."""
        cfg = ScrubSinkConfig(
            name="test_sink_export",
            palette_name="medbay_clean",
            wear_level=0.3
        )
        gen = ScrubSinkGenerator()
        obj = gen.generate(cfg)
        report = gen.validate(obj, cfg)

        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
        os.makedirs(out_dir, exist_ok=True)
        export_path = os.path.join(out_dir, "test_sink_export.glb")

        glb_path, json_path = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=report,
            filepath=export_path,
            generator_name="ScrubSinkGenerator"
        )

        self.assertTrue(os.path.exists(glb_path), f"GLB file was not created at {glb_path}")
        self.assertTrue(os.path.exists(json_path), f"JSON metadata file was not created at {json_path}")
        self.assertGreater(os.path.getsize(glb_path), 500, "GLB file is suspiciously small")

    def test_uv_layer_and_atlas_mapping_integrity(self):
        """Verify that generators across different families have valid UVMap layers and correctly mapped texture atlas rects."""
        test_cases = [
            (AutopsyTableConfig(name="test_uv_autopsy", palette_name="medbay_clean"), AutopsyTableGenerator()),
            (CrateConfig(name="test_uv_crate", palette_name="industrial_hazard"), CrateGenerator()),
            (TerminalConfig(name="test_uv_terminal", palette_name="command_bridge"), TerminalGenerator()),
            (CrashCartConfig(name="test_uv_crash_cart", palette_name="medbay_clean"), CrashCartGenerator()),
        ]

        for cfg, gen in test_cases:
            obj = gen.generate(cfg)
            report = gen.validate(obj, cfg)
            self.assertTrue(report.is_valid, f"Generator {gen.__class__.__name__} failed validation: {report.errors}")
            self.assertTrue(report.has_uv_map, f"Generator {gen.__class__.__name__} missing UV map")

            mesh = obj.data
            self.assertGreater(len(mesh.uv_layers), 0, f"Mesh {obj.name} must have at least 1 UV layer")
            uv_layer = mesh.uv_layers.active or mesh.uv_layers[0]
            self.assertEqual(uv_layer.name, "UVMap")

            uv_data = uv_layer.data
            non_zero_uv_count = 0
            for poly in mesh.polygons:
                mat = obj.material_slots[poly.material_index].material if poly.material_index < len(obj.material_slots) else None
                expected_rect = None
                if mat and "atlas_rect" in mat:
                    r = mat["atlas_rect"]
                    expected_rect = (r[0], r[1], r[2], r[3])

                for loop_idx in poly.loop_indices:
                    u, v = uv_data[loop_idx].uv
                    self.assertGreaterEqual(u, -0.01, f"UV U coordinate out of bounds in {obj.name}: {u}")
                    self.assertLessEqual(u, 1.01, f"UV U coordinate out of bounds in {obj.name}: {u}")
                    self.assertGreaterEqual(v, -0.01, f"UV V coordinate out of bounds in {obj.name}: {v}")
                    self.assertLessEqual(v, 1.01, f"UV V coordinate out of bounds in {obj.name}: {v}")
                    if abs(u) > 1e-4 or abs(v) > 1e-4:
                        non_zero_uv_count += 1

                    if expected_rect:
                        rx, ry, rw, rh = expected_rect
                        self.assertGreaterEqual(u, rx - 0.02, f"U coordinate {u} outside material rect X {rx} in {obj.name}")
                        self.assertLessEqual(u, rx + rw + 0.02, f"U coordinate {u} outside material rect X+W {rx+rw} in {obj.name}")
                        self.assertGreaterEqual(v, ry - 0.02, f"V coordinate {v} outside material rect Y {ry} in {obj.name}")
                        self.assertLessEqual(v, ry + rh + 0.02, f"V coordinate {v} outside material rect Y+H {ry+rh} in {obj.name}")

            self.assertGreater(non_zero_uv_count, 0, f"Mesh {obj.name} has no non-zero UV coordinates!")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
