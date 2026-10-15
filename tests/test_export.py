import unittest
import sys
import os
import json

# Ensure package root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
from procedural_assets.generators.electrical_panel.config import ElectricalPanelConfig
from procedural_assets.generators.electrical_panel.generator import ElectricalPanelGenerator
from procedural_assets.export.glb_exporter import GLBExporter

class TestExportPipeline(unittest.TestCase):

    def setUp(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.output_dir = os.path.join(parent_dir, "output", "test_run")
        os.makedirs(self.output_dir, exist_ok=True)
        self.generator = ElectricalPanelGenerator()

    def test_export_glb_and_json(self):
        """Test complete export pipeline producing valid GLB and JSON sidecar."""
        config = ElectricalPanelConfig(
            seed=4242,
            name="export_test_panel",
            width=0.75,
            height=0.95,
            depth=0.20,
            target_tri_budget=400
        )
        obj = self.generator.generate(config)
        report = self.generator.validate(obj, config)
        self.assertTrue(report.is_valid)

        glb_path = os.path.join(self.output_dir, f"{config.name}.glb")
        glb_out, json_out = GLBExporter.export(
            obj=obj,
            config=config,
            report=report,
            filepath=glb_path,
            generator_name="ElectricalPanelGenerator"
        )

        # Check GLB file
        self.assertTrue(os.path.exists(glb_out), f"GLB file should exist at {glb_out}")
        self.assertGreater(os.path.getsize(glb_out), 1000, "GLB file should have valid size (>1KB)")

        # Check JSON sidecar
        self.assertTrue(os.path.exists(json_out), f"JSON file should exist at {json_out}")
        with open(json_out, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["model_name"], config.name)
        self.assertEqual(meta["seed"], config.seed)
        self.assertEqual(meta["mesh_metrics"]["triangle_count"], report.triangle_count)
        self.assertEqual(meta["mesh_metrics"]["vertex_count"], report.vertex_count)
        self.assertIn("godot_4_compatibility", meta)

    def test_glb_reimport_into_blender(self):
        """Verify the exported GLB can be re-imported into Blender cleanly without data corruption."""
        config = ElectricalPanelConfig(seed=5555, name="reimport_panel")
        obj = self.generator.generate(config)
        report = self.generator.validate(obj, config)

        glb_path = os.path.join(self.output_dir, f"{config.name}.glb")
        GLBExporter.export(obj=obj, config=config, report=report, filepath=glb_path)

        # Clear scene completely
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.assertEqual(len(bpy.data.objects), 0)

        # Re-import GLB
        bpy.ops.import_scene.gltf(filepath=glb_path)
        self.assertGreater(len(bpy.data.objects), 0, "Scene must have imported objects")

        # Find mesh object
        imported_mesh_objs = [o for o in bpy.data.objects if o.type == 'MESH']
        self.assertGreater(len(imported_mesh_objs), 0, "At least one mesh object must be re-imported")

        imported_mesh = imported_mesh_objs[0].data
        self.assertGreater(len(imported_mesh.vertices), 0, "Imported mesh must have vertices")
        self.assertGreater(len(imported_mesh.polygons), 0, "Imported mesh must have polygons")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
