import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
from procedural_assets.generators import GENERATOR_REGISTRY
from procedural_assets.export.glb_exporter import GLBExporter

class TestMasterAssetFamilies(unittest.TestCase):

    def setUp(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.output_dir = os.path.join(parent_dir, "output", "test_families")
        os.makedirs(self.output_dir, exist_ok=True)

    def test_all_families_generation_and_export(self):
        """Test that all 8 procedural asset families generate valid geometry and export to GLB."""
        for family_name, (config_cls, generator_cls) in GENERATOR_REGISTRY.items():
            with self.subTest(family=family_name):
                bpy.ops.wm.read_factory_settings(use_empty=True)

                config = config_cls(seed=4242, name=f"test_{family_name}")
                gen = generator_cls()
                obj = gen.generate(config)

                report = gen.validate(obj, config)
                self.assertTrue(report.is_valid, f"Family '{family_name}' failed validation: {report.errors}")
                self.assertGreater(report.vertex_count, 0, f"Family '{family_name}' vertex count must be > 0")
                self.assertGreater(report.triangle_count, 0, f"Family '{family_name}' tri count must be > 0")
                self.assertTrue(report.has_vertex_colors, f"Family '{family_name}' must have vertex colors")

                # Budget compliance tolerance (1.20)
                budget_ratio = report.triangle_count / max(1, config.target_tri_budget)
                self.assertLessEqual(
                    budget_ratio,
                    1.20,
                    f"Family '{family_name}' exceeded budget: {report.triangle_count} vs {config.target_tri_budget} (ratio: {budget_ratio:.2f})"
                )

                # Export test
                glb_path = os.path.join(self.output_dir, f"{config.name}.glb")
                glb_out, json_out = GLBExporter.export(
                    obj=obj,
                    config=config,
                    report=report,
                    filepath=glb_path,
                    generator_name=generator_cls.__name__
                )

                self.assertTrue(os.path.exists(glb_out), f"GLB file for '{family_name}' must exist")
                self.assertGreater(os.path.getsize(glb_out), 1000, f"GLB for '{family_name}' must be > 1KB")
                self.assertTrue(os.path.exists(json_out), f"JSON for '{family_name}' must exist")

if __name__ == "__main__":
    unittest.main()
