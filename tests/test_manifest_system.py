"""
Unit tests for the Declarative Generator Manifest and Parameter Contract System.
Tests GeneratorManifest, ParameterDef, PresetDef, JSON parsing, validation,
and dynamic CLI argument processing.
"""

import unittest
import os
import sys
import json
import argparse

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from procedural_assets.core.manifest import (
    GeneratorManifest,
    ParameterDef,
    PresetDef,
    AuthorDef,
    discover_all_manifests,
    find_manifest_for_family,
)

class TestManifestSystem(unittest.TestCase):

    def test_parameter_def_validation_numeric(self):
        param_float = ParameterDef(
            key="width",
            label="Width",
            type="float",
            default=1.5,
            min=0.5,
            max=3.0,
            step=0.1
        )
        # Valid
        valid, err = param_float.validate_value(1.5)
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Min boundary failure
        valid, err = param_float.validate_value(0.2)
        self.assertFalse(valid)
        self.assertIn("less than minimum", err)

        # Max boundary failure
        valid, err = param_float.validate_value(4.0)
        self.assertFalse(valid)
        self.assertIn("exceeds maximum", err)

        # Type conversion
        valid, err = param_float.validate_value("not_a_float")
        self.assertFalse(valid)
        self.assertIn("Expected float", err)

    def test_parameter_def_validation_enum(self):
        param_enum = ParameterDef(
            key="bed_style",
            label="Bed Style",
            type="enum",
            default="standard",
            options=[
                {"value": "standard", "label": "Standard"},
                {"value": "bunk", "label": "Bunk"}
            ]
        )
        valid, err = param_enum.validate_value("standard")
        self.assertTrue(valid)

        valid, err = param_enum.validate_value("invalid_style")
        self.assertFalse(valid)
        self.assertIn("allowed options", err)

    def test_parameter_def_validation_rgba(self):
        param_rgba = ParameterDef(
            key="custom_color",
            label="Custom Color",
            type="color_rgba",
            default=[1.0, 0.0, 0.0, 1.0]
        )
        valid, err = param_rgba.validate_value([0.5, 0.5, 0.5, 1.0])
        self.assertTrue(valid)

        # Invalid length
        valid, err = param_rgba.validate_value([1.0, 0.0, 0.0])
        self.assertFalse(valid)

        # Invalid range (> 1.0)
        valid, err = param_rgba.validate_value([1.5, 0.0, 0.0, 1.0])
        self.assertFalse(valid)

    def test_autopsy_table_manifest_file(self):
        manifest = find_manifest_for_family("autopsy_table")
        self.assertIsNotNone(manifest, "autopsy_table manifest.json should be discovered")
        self.assertEqual(manifest.id, "below_nominal.medical.autopsy_table")
        self.assertEqual(manifest.license, "CC-BY-4.0")
        self.assertGreaterEqual(len(manifest.parameters), 10)
        self.assertGreaterEqual(len(manifest.presets), 2)

        # Validate preset values
        sterile = next((p for p in manifest.presets if p.id == "sterile_autopsy"), None)
        self.assertIsNotNone(sterile)
        self.assertEqual(sterile.values.get("table_type"), "standard_autopsy")
        self.assertTrue(sterile.values.get("overhead_lamp"))

    def test_crash_cart_manifest_file(self):
        manifest = find_manifest_for_family("crash_cart")
        self.assertIsNotNone(manifest, "crash_cart manifest.json should be discovered")
        self.assertEqual(manifest.id, "below_nominal.medical.crash_cart")
        self.assertIn("medical", manifest.tags)
        self.assertTrue(any(p.key == "drawer_count" for p in manifest.parameters))

        # Check export capabilities
        self.assertTrue(manifest.export_capabilities.get("supports_collision", False))
        self.assertEqual(manifest.export_capabilities.get("default_collision_suffix"), "-convcolonly")

    def test_discover_all_manifests(self):
        manifests = discover_all_manifests()
        self.assertGreaterEqual(len(manifests), 44, f"Expected at least 44 manifests, found {len(manifests)}")
        self.assertIn("autopsy_table", manifests)
        self.assertIn("crash_cart", manifests)
        self.assertIn("electrical_panel", manifests)
        self.assertIn("station_corridor", manifests)

        # Verify each manifest has basic required fields
        for family_name, m in manifests.items():
            self.assertTrue(m.id.startswith("below_nominal.") or m.id.startswith("community."), f"{family_name} id must start with below_nominal. or community.")
            self.assertGreater(len(m.parameters), 0, f"{family_name} must have parameters")
            self.assertGreater(len(m.presets), 0, f"{family_name} must have at least 1 preset")

    def test_manifest_validation_contract(self):
        manifest = find_manifest_for_family("autopsy_table")
        # Valid parameters
        valid, errors = manifest.validate_parameters({
            "length": 2.2,
            "overhead_lamp": True,
            "table_type": "standard_autopsy"
        })
        self.assertTrue(valid, f"Validation failed with errors: {errors}")
        self.assertEqual(len(errors), 0)

        # Invalid parameters
        valid, errors = manifest.validate_parameters({
            "length": 99.0, # Exceeds max 3.0
            "table_type": "hover_table" # Not in enum options
        })
        self.assertFalse(valid)
        self.assertEqual(len(errors), 2)

    def test_dynamic_argparse_integration(self):
        manifest = find_manifest_for_family("autopsy_table")
        parser = argparse.ArgumentParser()
        manifest.add_to_argparse(parser)

        # Simulate CLI inputs: --length 2.5 --no-overhead-lamp --table-type dissection_station
        cli_args = ["--length", "2.5", "--no-overhead-lamp", "--table-type", "dissection_station"]
        args = parser.parse_args(cli_args)

        kwargs = manifest.build_config_kwargs(args)
        self.assertEqual(kwargs.get("length"), 2.5)
        self.assertFalse(kwargs.get("overhead_lamp"))
        self.assertEqual(kwargs.get("table_type"), "dissection_station")

if __name__ == "__main__":
    unittest.main()
