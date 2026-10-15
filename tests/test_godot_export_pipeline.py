import unittest
import sys
import os
import json
import mathutils

# Ensure package root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
from procedural_assets.generators.office_door.config import OfficeDoorConfig
from procedural_assets.generators.office_door.generator import OfficeDoorGenerator
from procedural_assets.generators.scrub_sink.config import ScrubSinkConfig
from procedural_assets.generators.scrub_sink.generator import ScrubSinkGenerator
from procedural_assets.generators.crash_cart.config import CrashCartConfig
from procedural_assets.generators.crash_cart.generator import CrashCartGenerator
from procedural_assets.generators.electrical_panel.config import ElectricalPanelConfig
from procedural_assets.generators.electrical_panel.generator import ElectricalPanelGenerator
from procedural_assets.export.glb_exporter import GLBExporter, ExportResult
from procedural_assets.export.godot_validator import validate_glb_with_godot, is_godot_available

class TestGodotExportPipeline(unittest.TestCase):
    """
    Comprehensive verification suite for the glTF/GLB export pipeline to Godot 4.
    Tests pivot normalization, transform freezing, flat shading, multi-object hierarchy,
    collision shapes (-convcolonly / -colonly), sockets, export reports, and live Godot 4 import.
    """

    def setUp(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.output_dir = os.path.join(parent_dir, "output", "test_pipeline")
        os.makedirs(self.output_dir, exist_ok=True)

    def test_pivot_and_transform_normalization(self):
        """Verify that GLBExporter normalizes transforms and sets floor contact to Z = 0.0."""
        gen = ScrubSinkGenerator()
        cfg = ScrubSinkConfig(name="test_norm_sink", palette_name="medbay_clean")
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)

        glb_path = os.path.join(self.output_dir, f"{cfg.name}.glb")
        res = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="ScrubSinkGenerator"
        )

        # Check returned tuple unpacking compatibility
        self.assertIsInstance(res, ExportResult)
        self.assertTrue(os.path.exists(res.glb_path))
        self.assertTrue(os.path.exists(res.json_path))
        self.assertTrue(os.path.exists(res.report_json_path))
        self.assertTrue(os.path.exists(res.report_md_path))

        # Check transforms applied
        self.assertEqual(obj.location, mathutils.Vector((0, 0, 0)))
        self.assertEqual(obj.scale, mathutils.Vector((1, 1, 1)))

        # Check lowest vertex rests on Z = 0.0 (floor contact)
        min_z = min(v.co.z for v in obj.data.vertices)
        self.assertAlmostEqual(min_z, 0.0, places=3, msg="Floor prop lowest vertex must sit on Z=0.0")

    def test_normals_are_flat_shaded(self):
        """Verify authentic PS1 flat shading on all polygons."""
        gen = ElectricalPanelGenerator()
        cfg = ElectricalPanelConfig(name="test_flat_panel")
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)

        glb_path = os.path.join(self.output_dir, f"{cfg.name}.glb")
        GLBExporter.export(obj=obj, config=cfg, report=rep, filepath=glb_path)

        for poly in obj.data.polygons:
            self.assertFalse(poly.use_smooth, f"Polygon {poly.index} should have flat shading for PS1 aesthetic")

    def test_collision_mesh_generation_box_and_convex(self):
        """Verify Godot collision meshes are created with proper suffixes and parented to root."""
        gen = CrashCartGenerator()
        cfg = CrashCartConfig(
            name="test_cart_col",
            add_collision_mesh=True,
            collision_type="box",
            collision_suffix="-convcolonly"
        )
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)

        glb_path = os.path.join(self.output_dir, f"{cfg.name}.glb")
        res = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="CrashCartGenerator"
        )

        # Read JSON report to verify collision metadata
        with open(res.report_json_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        col_meta = report_data["collision"]
        self.assertTrue(col_meta["enabled"])
        self.assertEqual(col_meta["node_name"], f"{cfg.name}-convcolonly")
        self.assertEqual(col_meta["shape_type"], "box")
        self.assertEqual(col_meta["godot_suffix"], "-convcolonly")

    def test_live_godot_headless_import(self):
        """Execute real Godot 4 engine in headless mode to verify import, materials and hierarchy."""
        if not is_godot_available():
            self.skipTest("Godot 4 binary not installed on this host")

        gen = ScrubSinkGenerator()
        cfg = ScrubSinkConfig(
            name="test_godot_live_sink",
            palette_name="medbay_clean",
            add_collision_mesh=True,
            collision_suffix="-convcolonly"
        )
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)

        glb_path = os.path.join(self.output_dir, f"{cfg.name}.glb")
        res = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="ScrubSinkGenerator",
            validate_with_godot=True
        )

        # Inspect export report's godot validation block
        with open(res.report_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        godot_val = data["godot_4_validation"]
        self.assertTrue(godot_val.get("tested_in_godot"), "Must be tested in real Godot 4")
        self.assertTrue(godot_val.get("success"), f"Godot import should succeed: {godot_val.get('errors')}")
        self.assertGreater(godot_val.get("mesh_count", 0), 0, "Godot must recognize visual MeshInstance3D")
        self.assertGreater(godot_val.get("total_surfaces", 0), 0, "Godot mesh must have surfaces")
        self.assertGreater(len(godot_val.get("materials", [])), 0, "Godot surfaces must have materials")

        # Sockets check in Godot
        self.assertGreaterEqual(godot_val.get("socket_count", 0), 1, "Godot must recognize socket Node3D empties")

    def test_export_report_markdown_generation(self):
        """Verify the human-readable Markdown report contains all required sections."""
        gen = OfficeDoorGenerator()
        cfg = OfficeDoorConfig(name="test_door_report", palette_name="command_bridge")
        obj = gen.generate(cfg)
        rep = gen.validate(obj, cfg)

        glb_path = os.path.join(self.output_dir, f"{cfg.name}.glb")
        res = GLBExporter.export(
            obj=obj,
            config=cfg,
            report=rep,
            filepath=glb_path,
            generator_name="OfficeDoorGenerator"
        )

        with open(res.report_md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        self.assertIn("# Informe de Exportación a Godot 4", md_text)
        self.assertIn("## 1. Archivo y Dimensiones", md_text)
        self.assertIn("## 2. Normalización de Pipeline", md_text)
        self.assertIn("## 3. Jerarquía de Objetos", md_text)
        self.assertIn("## 4. Materiales Compactados", md_text)
        self.assertIn("## 5. Colisión para Godot 4", md_text)
        self.assertIn("## 6. Sockets / Puntos de Anclaje", md_text)
        self.assertIn("## 7. Validación Real en Motor Godot 4", md_text)

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
