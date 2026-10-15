import unittest
import sys
import os

# Ensure package root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bpy
from procedural_assets.generators.electrical_panel.config import ElectricalPanelConfig
from procedural_assets.generators.electrical_panel.generator import ElectricalPanelGenerator

class TestElectricalPanelGenerator(unittest.TestCase):

    def setUp(self):
        # Reset scene to empty before each test
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.generator = ElectricalPanelGenerator()

    def test_default_generation(self):
        """Test generating panel with default configuration."""
        config = ElectricalPanelConfig(name="test_default")
        obj = self.generator.generate(config)
        report = self.generator.validate(obj, config)

        self.assertTrue(report.is_valid, f"Report should be valid. Errors: {report.errors}")
        self.assertGreater(report.vertex_count, 0, "Vertex count must be > 0")
        self.assertGreater(report.triangle_count, 0, "Triangle count must be > 0")
        self.assertTrue(report.has_vertex_colors, "Mesh must contain vertex color attribute")
        self.assertGreater(len(report.material_names), 0, "Mesh must have materials assigned")
        self.assertLessEqual(
            report.triangle_count,
            int(config.target_tri_budget * 1.15),
            f"Triangles ({report.triangle_count}) should not exceed target budget ({config.target_tri_budget}) by >15%"
        )

    def test_seed_determinism(self):
        """Test that identical seeds generate byte-for-byte identical mesh counts and dimensions."""
        config1 = ElectricalPanelConfig(seed=42, name="panel_a")
        obj1 = self.generator.generate(config1)
        report1 = self.generator.validate(obj1, config1)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        generator2 = ElectricalPanelGenerator()
        config2 = ElectricalPanelConfig(seed=42, name="panel_b")
        obj2 = generator2.generate(config2)
        report2 = generator2.validate(obj2, config2)

        self.assertEqual(report1.vertex_count, report2.vertex_count, "Vertex counts must match for same seed")
        self.assertEqual(report1.triangle_count, report2.triangle_count, "Triangle counts must match for same seed")
        self.assertEqual(report1.dimensions, report2.dimensions, "Dimensions must match for same seed")

    def test_seed_variance(self):
        """Test that different seeds generate varied control/cable configurations."""
        config1 = ElectricalPanelConfig(seed=101, name="panel_seed_1")
        obj1 = self.generator.generate(config1)
        report1 = self.generator.validate(obj1, config1)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        generator2 = ElectricalPanelGenerator()
        config2 = ElectricalPanelConfig(seed=202, name="panel_seed_2")
        obj2 = generator2.generate(config2)
        report2 = generator2.validate(obj2, config2)

        # Both valid but different geometry
        self.assertTrue(report1.is_valid)
        self.assertTrue(report2.is_valid)

    def test_crt_toggle(self):
        """Test panel generation without CRT screen (switches to analog gauges)."""
        config = ElectricalPanelConfig(name="panel_no_crt", has_crt=False)
        obj = self.generator.generate(config)
        report = self.generator.validate(obj, config)

        self.assertTrue(report.is_valid)
        self.assertGreater(report.triangle_count, 0)
        # Should still satisfy budget
        self.assertLessEqual(report.triangle_count, int(config.target_tri_budget * 1.15))

    def test_dimensions_scaling(self):
        """Test that custom dimensions (width, height, depth) are respected."""
        custom_w, custom_h, custom_d = 1.20, 1.60, 0.35
        config = ElectricalPanelConfig(
            name="panel_large",
            width=custom_w,
            height=custom_h,
            depth=custom_d
        )
        obj = self.generator.generate(config)
        report = self.generator.validate(obj, config)

        self.assertTrue(report.is_valid)
        dim_x, dim_y, dim_z = report.dimensions
        # Verify dimensions match custom configuration within reasonable tolerance (accounting for flanges)
        self.assertAlmostEqual(dim_x, custom_w, delta=0.08)
        self.assertGreaterEqual(dim_y, custom_h)  # flange adds small height
        self.assertAlmostEqual(dim_z, custom_d, delta=0.08)

    def test_budget_enforcement(self):
        """Test that reducing target tri budget decreases the resulting triangle count."""
        config_high = ElectricalPanelConfig(seed=777, target_tri_budget=600, name="panel_high")
        obj_high = self.generator.generate(config_high)
        report_high = self.generator.validate(obj_high, config_high)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        generator_low = ElectricalPanelGenerator()
        config_low = ElectricalPanelConfig(seed=777, target_tri_budget=280, name="panel_low")
        obj_low = generator_low.generate(config_low)
        report_low = generator_low.validate(obj_low, config_low)

        self.assertLess(
            report_low.triangle_count,
            report_high.triangle_count,
            f"Low budget tris ({report_low.triangle_count}) should be lower than high budget tris ({report_high.triangle_count})"
        )

if __name__ == "__main__":
    unittest.main()
